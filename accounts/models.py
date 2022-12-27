from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Profile(models.Model):
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True, verbose_name='Аватарка')
    github = models.URLField(max_length=50, null=True, blank=True, verbose_name='Ссылка на github')
    about = models.TextField(max_length=2000, null=True, blank=True, verbose_name='О себе')
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name='пользователь', related_name='profile')

    def __str__(self):
        return self.user.get_full_name() + "'s Profile"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

        permissions = [
            ('can_view_all_users', 'Может видеть всех пользователей'),
        ]