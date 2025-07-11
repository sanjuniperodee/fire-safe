# Generated by Django 4.2.6 on 2024-01-12 09:24

import auths.validators
from django.db import migrations, models
import storages.backends.s3boto3


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0003_alter_customuser_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar_url',
            field=models.ImageField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(location='avatars/'), upload_to='avatars/', validators=[auths.validators.validate_file_extension]),
        ),
    ]
