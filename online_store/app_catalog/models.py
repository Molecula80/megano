from django.db import models


class Category(models.Model):
    parent = models.ForeignKey('Category', blank=True, null=True, on_delete=models.SET_NULL, related_name='children',
                               verbose_name='родитель')
    title = models.CharField(max_length=255, verbose_name='название')
    sort_index = models.PositiveIntegerField(verbose_name='индекс сортировки')
    icon = models.ImageField(upload_to='images/icons/', blank=True, null=True, verbose_name='иконка')
    active = models.BooleanField(default=False, verbose_name='активно')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.title
