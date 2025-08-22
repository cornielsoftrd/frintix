from django.core.management.base import BaseCommand
from shared_core.models import Company, User
from public_apps.models import Client, Domain


class Command(BaseCommand):
    help = "Crea un nuevo tenant con su company, dominio y usuario admin"

    def add_arguments(self, parser):
        parser.add_argument('schema_name', type=str, help="Nombre del schema (subdominio)")
        parser.add_argument('company_name', type=str, help="Nombre de la empresa / restaurante")
        parser.add_argument('domain', type=str, help="Dominio para el tenant")
        parser.add_argument('admin_email', type=str, help="Email del usuario admin")
        parser.add_argument('admin_password', type=str, help="Contraseña del usuario admin")

    def handle(self, *args, **options):
        schema_name = options['schema_name']
        company_name = options['company_name']
        domain = options['domain']
        admin_email = options['admin_email']
        admin_password = options['admin_password']

        # 1. Crear Company
        company = Company.objects.create(name=company_name)

        # 2. Crear Client (Tenant)
        tenant = Client.objects.create(
            schema_name=schema_name,
            name=company_name,
            company=company,
            paid_until="2025-09-09",
            on_trial=True
        )
        tenant.save()

        # 3. Crear Domain
        Domain.objects.create(
            domain=domain,
            tenant=tenant,
            is_primary=True
        )

        # 4. Crear Usuario admin vinculado a la Company
        User.objects.create_user(
            username="admin",
            email=admin_email,
            password=admin_password,
            role="admin",
            company=company
        )

        self.stdout.write(self.style.SUCCESS(f"Tenant '{schema_name}' creado con éxito."))
