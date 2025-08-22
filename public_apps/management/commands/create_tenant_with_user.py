from django.core.management.base import BaseCommand
from django_tenants.utils import schema_context
from public_apps.models import Client, Domain
from shared_core.models import Company, User

class Command(BaseCommand):
    help = "Crea un tenant con su dominio, company y usuario admin"

    def add_arguments(self, parser):
        parser.add_argument("schema_name", type=str, help="Nombre del schema del tenant")
        parser.add_argument("tenant_name", type=str, help="Nombre visible del tenant")
        parser.add_argument("domain", type=str, help="Dominio para el tenant")
        parser.add_argument("admin_email", type=str, help="Email del usuario admin")
        parser.add_argument("admin_password", type=str, help="Password del usuario admin")

    def handle(self, *args, **options):
        schema_name = options["schema_name"]
        tenant_name = options["tenant_name"]
        domain_name = options["domain"]
        admin_email = options["admin_email"]
        admin_password = options["admin_password"]

        # 1️⃣ Crear la compañía
        company = Company.objects.create(name=tenant_name)
        self.stdout.write(self.style.SUCCESS(f"✅ Company creada: {company.name}"))

        # 2️⃣ Crear el tenant (Client)
        tenant = Client.objects.create(
            schema_name=schema_name,
            name=tenant_name,
            company=company,
            paid_until="2025-09-09",
            on_trial=True
        )
        tenant.save()
        self.stdout.write(self.style.SUCCESS(f"✅ Tenant creado: {tenant.schema_name}"))

        # 3️⃣ Crear el dominio
        Domain.objects.create(
            domain=domain_name,
            tenant=tenant,
            is_primary=True
        )
        self.stdout.write(self.style.SUCCESS(f"✅ Dominio creado: {domain_name}"))

        # 4️⃣ Crear el usuario admin en el schema del tenant
        with schema_context(schema_name):
            User.objects.create_superuser(
                email=admin_email,
                password=admin_password,
                company=company,
                role="restaurant_admin"
            )
        self.stdout.write(self.style.SUCCESS(f"✅ Usuario admin creado: {admin_email}"))

        self.stdout.write(self.style.SUCCESS("🎉 Tenant con usuario admin creado exitosamente"))
