from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Group(models.Model):
    """Сообщество (группа) для публикаций."""
    title = models.CharField("Название", max_length=200)
    slug = models.SlugField(
        "Идентификатор (slug)",
        max_length=50,
        unique=True,
        help_text="Только латиница, цифры, дефис и подчёркивание",
    )
    description = models.TextField("Описание")

    class Meta:
        ordering = ("title",)
        verbose_name = "группа"
        verbose_name_plural = "группы"

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    """Публикация пользователя."""
    text = models.TextField("Текст публикации")
    pub_date = models.DateTimeField(
        "Дата публикации",
        auto_now_add=True,
        db_index=True,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор",
    )
    image = models.ImageField(
        "Картинка",
        upload_to="posts/",
        blank=True,
        null=True,
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name="posts",
        verbose_name="Группа",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "публикация"
        verbose_name_plural = "публикации"

    def __str__(self) -> str:
        return self.text[:15]


class Comment(models.Model):
    """Комментарий к публикации."""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Публикация",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    text = models.TextField("Текст комментария")
    created = models.DateTimeField(
        "Дата добавления",
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ("-created",)
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"

    def __str__(self) -> str:
        return self.text[:15]


class Follow(models.Model):
    """Подписка одного пользователя на другого."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="follower",   # кто подписывается
        verbose_name="Подписчик",
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following",  # на кого подписан
        verbose_name="Автор",
    )

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "подписки"
        constraints = (
            # уникальная пара подписчик → автор
            models.UniqueConstraint(
                fields=("user", "following"),
                name="unique_user_following",
            ),
        )

    def clean(self):
        # Защитимся от self-follow на уровне модели
        if self.user_id == self.following_id:
            raise ValidationError("Нельзя подписаться на самого себя.")

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user} → {self.following}"
