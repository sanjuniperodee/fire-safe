from django.core.management.base import BaseCommand
from django.utils import timezone

from objects.models import Complaint


class Command(BaseCommand):
    help = 'Debug complaints status and expiration dates'

    def handle(self, *args, **options):
        now = timezone.now()
        complaints = Complaint.objects.all()
        for complaint in complaints:
            self.stdout.write(f"Complaint {complaint.unique_id}:")
            self.stdout.write(f"  Status: {complaint.status}")
            self.stdout.write(f"  Expiration Date: {complaint.expiration_date}")
            self.stdout.write(f"  Is Expired: {complaint.expiration_date <= now}")
            self.stdout.write("")