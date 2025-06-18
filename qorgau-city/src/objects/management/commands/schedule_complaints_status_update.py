from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class Command(BaseCommand):
    help = 'Schedule the update_complaints_status task to run hourly'

    def handle(self, *args, **options):
        # schedule, _ = IntervalSchedule.objects.get_or_create(
        #     every=1,
        #     period=IntervalSchedule.HOURS,
        # )
        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=10,
            period=IntervalSchedule.MINUTES,
        )

        # Use code below to test faster
        # schedule, _ = IntervalSchedule.objects.get_or_create(
        #     every=10,
        #     period=IntervalSchedule.SECONDS,
        # )

        PeriodicTask.objects.get_or_create(
            interval=schedule,
            name='Update expired complaints',
            task='objects.tasks.update_complaints',
        )

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully scheduled update_complaints task'
            )
        )