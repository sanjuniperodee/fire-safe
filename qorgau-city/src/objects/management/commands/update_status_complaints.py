import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from objects.models import Complaint

import objects

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Update expired complaints from PENDING to NOT_ANSWERED and from ANSWERED to EXPIRED'

    def handle(self, *args, **options):
        logger.info("Starting update_status_complaints command")
        logger.info(f"Complaint: {Complaint.objects.all()}")
        # logger.info(f"Complaint: {Complaint.objects.get(id=1)}")

        not_answered_or_expired_complaints = Complaint.objects.filter(
            expiration_date__lte=timezone.now(),
            status=objects.Status.PENDING
        )
        logger.info(f"Found {not_answered_or_expired_complaints.count()} complaints to process")

        # Check for NOT_ANSWERED complaints.
        not_answered_count = 0
        for complaint in not_answered_or_expired_complaints:
            old_status = complaint.status

            complaint.mark_as_not_answered()
            if complaint.status != old_status:
                not_answered_count += 1
                logger.info(f"Updated complaint {complaint.unique_id} from {old_status} to {complaint.status}")

        logger.info(f'Successfully updated {not_answered_count} not_answered complaints')

        expired_count = 0
        # Check for EXPIRED complaints.
        for complaint in not_answered_or_expired_complaints:
            old_status = complaint.status
            complaint.mark_as_expired()
            if complaint.status != old_status:
                expired_count += 1
                logger.info(f"Updated complaint {complaint.unique_id} from {old_status} to {complaint.status}")

        logger.info(f'Successfully archived {expired_count} expired complaints')
        logger.info("Finished update_expired_complaints command")