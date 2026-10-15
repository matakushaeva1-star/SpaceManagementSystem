import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название ресурса')),
                ('resource_type', models.CharField(choices=[('room', 'Переговорная комната'), ('parking', 'Парковочное место')], max_length=10, verbose_name='Тип')),
                ('description', models.TextField(blank=True, verbose_name='Описание / Оборудование')),
                ('is_active', models.BooleanField(default=True, verbose_name='Доступен для бронирования')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateField(verbose_name='Дата бронирования')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Сотрудник')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.resource', verbose_name='Ресурс')),
            ],
        ),
    ]
