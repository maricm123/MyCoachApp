from django.shortcuts import get_object_or_404
import stripe
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from django.conf import settings
from django.http import JsonResponse
from subscription.models.payment_method import PaymentMethod
from subscription.models.subscribe import Subscribe
from subscription.models.coach_transaction import CoachTransaction
from subscription.payment.stripe_handler import create_subscription, detach_payment_card_from_id
from trainingProgram.models.training_program import TrainingProgram
from profiles.models.client import Client
from rest_framework import generics
from api_coach.shared_serializers import ListPaymentMethodSerializer, PaymentMethodSerializer
from django.db import transaction

from api_coach.serializers.serializers_subscribe import AddPaymentMethodToClientSerializer, DefaultCardSerializer

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

        # Save subscription details in your model
        subscription_instance = Subscribe.objects.create(
            client=client,
            training_program=program,
            coach_share_percentage=program.coach_share_percentage,
            stripe_subscription_id=subscription.id,
            status=subscription.status,
        )
        # Create a transaction record for the coach's share
        CoachTransaction.objects.create(
            coach=program.coach,
            amount=program.coach_share_percentage,
            subscription=subscription_instance,
        )
        return Response({'message': 'Subscription created successfully'})


class WebHook(APIView):
    def post(self, request):
        """
            This API handling the webhook .

            :return: returns event details as json response .
        """
        request_data = json.loads(request.body)
        if webhook_secret:
            # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
            signature = request.META['HTTP_STRIPE_SIGNATURE']
            try:
                event = stripe.Webhook.construct_event(
                    payload=request.body,
                    sig_header=signature,
                    secret=webhook_secret
                )
                data = event['data']
            except ValueError as err:
                raise err
            except stripe.error.SignatureVerificationError as err:
                raise err
            # Get the type of webhook event sent - used to check the status of PaymentIntents.
            event_type = event['type']
        else:
            data = request_data['data']
            event_type = request_data['type']
        data_object = data['object']

        if event_type == 'checkout.session.completed':
            # Payment is successful and the subscription is created.
            # You should provision the subscription and save the customer ID to your database.
            print("-----checkout.session.completed----->", data['object']['customer'])
        elif event_type == 'invoice.paid':
            # Continue to provision the subscription as payments continue to be made.
            # Store the status in your database and check when a user accesses your service.
            # This approach helps you avoid hitting rate limits.
            print("-----invoice.paid----->", data)
        elif event_type == 'invoice.payment_failed':
            # The payment failed or the customer does not have a valid payment method.
            # The subscription becomes past_due. Notify your customer and send them to the
            # customer portal to update their payment information.
            print("-----invoice.payment_failed----->", data)
        else:
            print('Unhandled event type {}'.format(event_type))

        return JsonResponse(success=True, safe=False)
