from django.db import models


class BlogPost(models.Model):

    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок",
        help_text="Напишите заголовок публикации",
    )
    content = models.TextField(
        verbose_name="Содержимое публикации",
        help_text="Напишите статью для публикации",
    )
    preview_image = models.ImageField(
        upload_to='blog/previews_images/',
        verbose_name='Превью (изображение)',
        help_text='Добавьте изображение',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True,
    )
    is_published = models.BooleanField(
        verbose_name="Опубликовано",
        default=False,
    )
    views_count = models.PositiveIntegerField(
        verbose_name="Всего просмотров",
        default=0,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Публикация блога"
        verbose_name_plural = "Публикации блога"
        ordering = ['-created_at']
