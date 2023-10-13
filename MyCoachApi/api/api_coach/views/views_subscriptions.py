from django.shortcuts import get_object_or_404
import stripe
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from django.conf import settings
from django.http import JsonResponse
from profiles.models.user import User
from api_coach.mixins import convert_stripe_period_to_date
from subscription.models.payment_method import PaymentMethod
from subscription.models.subscribe import Subscribe
from subscription.models.coach_transaction import CoachTransaction
from subscription.payment.stripe_handler import create_subscription, detach_payment_card_from_id, retrieve_payments_from_customer_id, retrieve_subscribe_from_id
from trainingProgram.models.training_program import TrainingProgram
from profiles.models.client import Client
from rest_framework import generics
from api_coach.shared_serializers import ListPaymentMethodSerializer, PaymentMethodSerializer
from django.db import transaction

from api_coach.serializers.serializers_subscribe import AddPaymentMethodToClientSerializer, ClientSubscribeListSerializer, DefaultCardSerializer, PaymentIntentSerializer

webhook_secret = settings.STRIPE_WEBHOOK_SECRET
stripe.api_key = settings.STRIPE_SECRET_KEY


class AddPaymentMethodToClientView(APIView):
    def post(self, request):
        serializer = AddPaymentMethodToClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=HTTP_201_CREATED)


class PaymentMethodList(generics.ListAPIView):
    serializer_class = ListPaymentMethodSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        client = Client.objects.get(user=user)
        return PaymentMethod.objects.get_payment_methods_for_client(client=client)
    

class SubscribeList(generics.ListAPIView):
    serializer_class = ClientSubscribeListSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """
        This view should return a list of all the subscribes
        for the currently authenticated user.
        """
        stripe_subscription_ids = []
        user = self.request.user
        client = Client.objects.get(user=user)
        subscribes = Subscribe.objects.subscribes_by_client(client=client)
        for subscribe in subscribes:
            stripe_subscription_id = subscribe.stripe_subscription_id
            stripe_subscription_ids.append(stripe_subscription_id)
        retrive_stripe_subscribe = retrieve_subscribe_from_id(stripe_subscription_ids)
        return subscribes
    
from datetime import datetime
class PaymentList(APIView):
    pass
    # permission_classes = (IsAuthenticated, )

    # def get(self, request):
    #     """
    #     This view should return a list of all the payments
    #     for the currently authenticated user.
    #     """
    #     user = self.request.user
    #     client = Client.objects.get(user=user)
    #     stripe_payments = retrieve_payments_from_customer_id(client.stripe_customer_id)

    #     payment_data = []
    #     for payment in stripe_payments:
    #         created = datetime.utcfromtimestamp(payment.created)
    #         data = {
    #             'payment': payment,
    #             'created': created,
    #         }
    #         serializer = PaymentIntentSerializer(data=data)
    #         serializer.is_valid()
    #         print(serializer.data)
    #         payment_data.append(serializer.data)
    #     return Response(payment_data, status=HTTP_200_OK)


class SetPaymentMethodDefault(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = DefaultCardSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        return Response(status=HTTP_200_OK)


class DeletePaymentMethod(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    
    @transaction.atomic
    def delete(self, request, pk):
        user = self.request.user
        client = Client.objects.get(user=user)
        payment_method = PaymentMethod.objects.filter(id=pk, client=client)
        stripe_payment_method_id = payment_method.first().stripe_payment_method_id
        try:
            detach_payment_card_from_id(stripe_payment_method_id)
            payment_method.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)


class CreateSubscription(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        client = Client.objects.get(user=user)
        price_id = request.data['price_id_stripe']
        # Fetch the program details
        program = TrainingProgram.objects.get(price_id_stripe=price_id)
        # Create a subscription in Stripe
        subscription = create_subscription(client, program)

        current_period_date = convert_stripe_period_to_date(subscription.current_period_end)

        # Save subscription details in your model
        subscription_instance = Subscribe.objects.create(
            client=client,
            training_program=program,
            coach_share_percentage=program.coach_share_percentage,
            stripe_subscription_id=subscription.id,
            status=subscription.status,
            current_period_end=current_period_date
        )
        # Create a transaction record for the coach's share
        CoachTransaction.objects.create(
            coach=program.coach,
            amount=program.coach_share_percentage,
            subscription=subscription_instance,
        )
        return Response({'message': 'Subscription created successfully'})


from django.views.decorators.csrf import csrf_exempt
class StripeWebHookView(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']

        # Replace 'YOUR_STRIPE_WEBHOOK_SECRET' with your actual webhook secret key
        endpoint_secret = 'whsec_cb52007df8cfbceddf02a35291b57bb0f76be42d93bf02e9a910bb4676a8bca2'

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            return Response({'error': 'Invalid payload'}, status=400)
        except stripe.error.SignatureVerificationError as e:
            return Response({'error': 'Invalid signature'}, status=400)

        # Handle the specific event types you want to process
        event_type = event['type']

        if event_type == 'customer.subscription.updated':
            print("SUB UPDATED")
            # Handle subscription update event
            # Access event data using event['data']['object']
            # Implement your logic here
            pass

        if event_type == 'customer.subscription.deleted':
            print("DELETED SUB")
            # Handle subscription update event
            # Access event data using event['data']['object']
            # Implement your logic here
            pass

        elif event_type == 'invoice.payment_succeeded':
            # Handle successful payment event
            # Access event data using event['data']['object']
            # Implement your logic here
            pass

        elif event_type == 'invoice.payment_failed':
            # Handle failed payment event
            # Access event data using event['data']['object']
            # Implement your logic here
            pass

        # Return a successful response
        return Response({'message': 'Webhook event processed'}, status=200)
