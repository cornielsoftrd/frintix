from django.contrib.auth.backends import ModelBackend
from shared_core.models import User
from public_apps.models import Domain

BASE_HOSTS = ["localhost", "127.0.0.1"]  # URLs where login is allowed for any user

class TenantAwareBackend(ModelBackend):
    def authenticate(self, request=None, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get("email") or kwargs.get("username")
        if not username or not password:
            return None

        domain = None
        if request:
            domain = getattr(request, "get_host", lambda: None)()
            if not domain:
                domain = request.META.get("HTTP_HOST")
            if domain:
                domain = domain.split(":")[0]

        try:
            if domain in BASE_HOSTS or domain is None:
                # Login from base URL, allow any user
                user = User.objects.get(email=username)
            else:
                # Login from tenant URL, user must belong to tenant
                tenant_domain = Domain.objects.filter(domain=domain).first()
                if not tenant_domain:
                    return None
                tenant_company = tenant_domain.tenant.company
                user = User.objects.get(email=username, company=tenant_company)
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
