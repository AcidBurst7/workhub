from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    full_name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=20, null=True)
    old_user_id = models.IntegerField(null=False, default=0)

    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'
