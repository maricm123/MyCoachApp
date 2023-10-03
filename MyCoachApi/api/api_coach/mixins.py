
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
