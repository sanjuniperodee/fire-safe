import logging

from celery import shared_task
from django.core.management import call_command

logger = logging.getLogger(__name__)


@shared_task
def update_complaints():
    logger.info("Starting update_complaints task")
    try:
        # call_command('update_expired_complaints')
        call_command('update_status_complaints')
        logger.info("update_status_complaints command completed successfully")
    except Exception as e:
        logger.error(f"Error in update_complaints task: {str(e)}")
    logger.info("Finished update_complaints task")
