from django.db import models
from django.contrib.auth.models import User

class Resource(models.Model):
    TYPE_CHOICES = [
        ('room', 'Переговорная комната'),
        ('parking', 'Парковочное место'),
    ]

    name = models.CharField(max_length=100, verbose_name="Название ресурса")
    resource_type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="Тип")
    description = models.TextField(blank=True, verbose_name="Описание / Оборудование")
    is_active = models.BooleanField(default=True, verbose_name="Доступен для бронирования")

    def __str__(self):
        return f"{self.get_resource_type_display()} — {self.name}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Сотрудник")
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, verbose_name="Ресурс")
    booking_date = models.DateField(verbose_name="Дата бронирования")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")

    def __str__(self):
        return f"{self.user.username} забронировал {self.resource.name} на {self.booking_date}"
