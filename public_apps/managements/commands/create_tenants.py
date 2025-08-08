from django.core.management.base import BaseCommand
from public_apps.models import Client, Domain
from shared_core.models import User

class Command(BaseCommand):
    help = "Create tenant and admin user"

    def add_arguments(self, parser):
        parser.add_argument('--schema', required=True)
        parser.add_argument('--name', required=True)
        parser.add_argument('--domain', required=True)
        parser.add_argument('--admin-email', required=True)
        parser.add_argument('--admin-pass', required=True)

    def handle(self, *args, **options):
        schema = options['schema']
        name = options['name']
        domain = options['domain']
        admin_email = options['admin_email']
        admin_pass = options['admin_pass']

        client = Client(schema_name=schema, name=name)
        client.save()
        Domain.objects.create(domain=domain, tenant=client, is_primary=True)
        User.objects.create_user(email=admin_email, password=admin_pass, role='restaurant_admin')
        self.stdout.write(self.style.SUCCESS('Tenant created'))
