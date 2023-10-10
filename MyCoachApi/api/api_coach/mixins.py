from datetime import datetime
"""
Accessing Request Data:
You can use this mixin when you need to access data from the incoming HTTP request, such as the user making the request, request headers, query parameters, or other request-related information.
Custom Validation:
It can be useful for custom validation logic in serializers. For example, you might want to validate a field based on the current user's permissions or some other request-specific information.
Custom Field Logic:
You might need to perform custom logic for a serializer field based on request data. For instance, you may want to show or hide certain fields based on the user making the request.
"""
class ReqContextMixin:
    @property
    def _req_context(self):
        return self.context["request"]


def convert_stripe_period_to_date(current_period_end):
    next_payment_date = datetime.utcfromtimestamp(current_period_end)
    formatted_next_payment_date = next_payment_date.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_next_payment_date
