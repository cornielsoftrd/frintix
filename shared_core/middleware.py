# shared_core/middleware.py
from django_tenants.utils import get_tenant_model

class TenantHeaderMiddleware:
    """
    Attach tenant to request if X-Tenant-Schema header is present.
    Safe at import time.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        schema_name = request.headers.get("X-Tenant-Schema")
        request.tenant = None

        if schema_name:
            TenantModel = get_tenant_model()
            try:
                tenant = TenantModel.objects.get(schema_name=schema_name)
                request.tenant = tenant
            except TenantModel.DoesNotExist:
                request.tenant = None

        return self.get_response(request)
