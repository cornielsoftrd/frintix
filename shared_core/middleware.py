class TenantHeaderMiddleware:
    """
    Attach tenant from X-Tenant-Schema only if not already attached by django-tenants.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only attach if tenant is not set
        if not hasattr(request, 'tenant') or request.tenant is None:
            schema_name = request.headers.get("X-Tenant-Schema")
            if schema_name:
                from django_tenants.utils import get_tenant_model
                TenantModel = get_tenant_model()
                try:
                    tenant = TenantModel.objects.get(schema_name=schema_name)
                    request.tenant = tenant
                except TenantModel.DoesNotExist:
                    from django.http import HttpResponseForbidden
                    return HttpResponseForbidden(f"Tenant '{schema_name}' does not exist.")

        return self.get_response(request)