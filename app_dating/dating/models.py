# noinspection PyUnresolvedReferences
from django.contrib.auth.models import AbstractUser
# noinspection PyUnresolvedReferences
from django.db import models
# noinspection PyUnresolvedReferences
from django.core.validators import MinValueValidator, MaxValueValidator
# noinspection PyUnresolvedReferences
from .validators import validate_age, validate_city


class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский')
    ]

    STATUS_CHOICES = [
        ('looking', 'В поиске'),
        ('busy', 'Занят'),
        ('complicated', 'Все сложно')
    ]

    username = models.CharField(max_length=150, unique=True, blank=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Пол')
    age = models.PositiveIntegerField(
        validators=[validate_age],
        verbose_name='Возраст'
    )
    city = models.CharField(
        max_length=100,
        validators=[validate_city],
        verbose_name='Город'
    )
    hobbies = models.TextField(blank=True, verbose_name='Увлечения')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='looking',
        verbose_name='Статус'
    )
    likes_count = models.PositiveIntegerField(default=0, verbose_name='Лайки')
    is_private = models.BooleanField(default=False, verbose_name='Приватный профиль')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender', 'age', 'city']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        indexes = [
            models.Index(fields=['gender', 'age', 'city', 'status']),
            models.Index(fields=['-likes_count']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class UserPhoto(models.Model):
    user = models.ForeignKey(
        User,
        related_name='photos',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    photo = models.ImageField(
        upload_to='user_photos/%Y/%m/%d/',
        verbose_name='Фотография'
    )
    is_main = models.BooleanField(default=False, verbose_name='Главное фото')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Фотография пользователя'
        verbose_name_plural = 'Фотографии пользователей'
        ordering = ['-is_main', 'uploaded_at']

    def __str__(self):
        return f"Фото {self.user.email}"

    def save(self, *args, **kwargs):
        """При сохранении фото проверяем, чтобы было только одно главное фото"""
        if self.is_main:
            # Убираем главный статус у других фото этого пользователя
            UserPhoto.objects.filter(
                user=self.user,
                is_main=True
            ).update(is_main=False)
        super().save(*args, **kwargs)


class UserInteraction(models.Model):
    INTERACTION_CHOICES = [
        ('like', 'Лайк'),
        ('dislike', 'Дизлайк'),
        ('view', 'Просмотр')
    ]

    from_user = models.ForeignKey(
        User,
        related_name='sent_interactions',
        on_delete=models.CASCADE,
        verbose_name='От пользователя'
    )
    to_user = models.ForeignKey(
        User,
        related_name='received_interactions',
        on_delete=models.CASCADE,
        verbose_name='К пользователю'
    )
    interaction_type = models.CharField(
        max_length=10,
        choices=INTERACTION_CHOICES,
        verbose_name='Тип взаимодействия'
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Взаимодействие'
        verbose_name_plural = 'Взаимодействия'
        unique_together = ['from_user', 'to_user', 'interaction_type']
        indexes = [
            models.Index(fields=['from_user', 'interaction_type']),
            models.Index(fields=['to_user', 'interaction_type']),
            models.Index(fields=['timestamp']),
        ]
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({self.interaction_type})"


class Match(models.Model):
    users = models.ManyToManyField(
        User,
        related_name='matches',
        verbose_name='Пользователи'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    last_interaction = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Мэтч'
        verbose_name_plural = 'Мэтчи'
        ordering = ['-last_interaction']

    def __str__(self):
        user_emails = [user.email for user in self.users.all()]
        return f"Match: {', '.join(user_emails)}"


class ContactExchange(models.Model):
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name='contact_exchanges',
        verbose_name='Мэтч'
    )
    initiator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='initiated_contacts',
        verbose_name='Инициатор'
    )
    contact_info = models.TextField(verbose_name='Контактная информация')
    message = models.TextField(blank=True, verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False, verbose_name='Принято')
    accepted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Обмен контактами'
        verbose_name_plural = 'Обмены контактами'
        ordering = ['-created_at']

    def __str__(self):
        return f"Contact exchange in match {self.match.id}"
