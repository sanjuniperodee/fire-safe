# Generated manually to fix author_name null constraint

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='author_name',
            field=models.CharField(blank=True, default='User', max_length=255),
        ),
    ] 