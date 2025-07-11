# Generated by Django 4.2.6 on 2025-06-18 19:43

import auths.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('statements', '0002_remove_statementprovider_is_accepted_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='statement',
            options={'verbose_name': 'заказ собственника', 'verbose_name_plural': 'заказы собственников'},
        ),
        migrations.AlterModelOptions(
            name='statementmedia',
            options={'verbose_name': 'медиафайл заявки собственника', 'verbose_name_plural': 'медиафайлы заявки собственников'},
        ),
        migrations.AddField(
            model_name='statement',
            name='is_busy_by_provider',
            field=models.BooleanField(default=False, verbose_name='Статус в работе провайдером или сделано'),
        ),
        migrations.AddField(
            model_name='statementprovider',
            name='archive_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='дата архива заявки(истек срок)'),
        ),
        migrations.AddField(
            model_name='statementprovider',
            name='chat_room_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='ID комнаты чата провайдера и собственника'),
        ),
        migrations.AddField(
            model_name='statementprovider',
            name='status',
            field=models.CharField(choices=[('OPENED', 'Открыто'), ('IN_WORK', 'В работе'), ('COMPLETED', 'Выполнено'), ('ARCHIVED', 'В архиве')], default='OPENED', max_length=20, verbose_name='статус заявки'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Составитель заявки'),
        ),
        migrations.AlterField(
            model_name='statementmedia',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='statement_media/', validators=[auths.validators.validate_files_extension]),
        ),
        migrations.CreateModel(
            name='StatementSuggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('chat_room_id', models.IntegerField(blank=True, null=True, verbose_name='ID комнаты чата провайдера и собственника')),
                ('status', models.CharField(choices=[('OPENED', 'Открыто'), ('IN_WORK', 'В работе'), ('COMPLETED', 'Выполнено'), ('ARCHIVED', 'В архиве')], default='OPENED', max_length=20, verbose_name='статус заявки')),
                ('archive_date', models.DateTimeField(blank=True, null=True, verbose_name='дата архива заявки(истек срок)')),
                ('provider', models.ForeignKey(limit_choices_to={'role__role': 'PROVIDER'}, on_delete=django.db.models.deletion.CASCADE, related_name='received_suggestions', to=settings.AUTH_USER_MODEL, verbose_name='Поставщик')),
                ('statement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_suggestions', to='statements.statement', verbose_name='Заявка')),
            ],
            options={
                'verbose_name': 'Предложение автора заявки к провайдеру',
                'verbose_name_plural': 'Предложения авторов заявок к провайдерам',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='StatementRequestForCompleted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('is_completed', models.BooleanField(default=False, verbose_name='Статус запроса на выполнено')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Поставщик')),
                ('statement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='statements.statement', verbose_name='Заявка')),
            ],
            options={
                'verbose_name': 'Запрос заказа на Выполнено от Провайдера',
                'verbose_name_plural': 'Запросы заказов на Выполнено от Провайдеров',
            },
        ),
        migrations.CreateModel(
            name='SeenStatement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen_at', models.DateTimeField(auto_now_add=True)),
                ('statement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='statements.statement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'statement')},
            },
        ),
    ]
