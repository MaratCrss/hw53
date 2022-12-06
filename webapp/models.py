from django.db import models
from django.urls import reverse


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        abstract = True


class TypeModel(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name="Название")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = "type"
        verbose_name = "Тип"
        verbose_name_plural = "Типы"


class StatusModel(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name="Название")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = "status"
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class IssueModel(BaseModel):
    title = models.CharField(max_length=50, verbose_name="Краткое описание")
    content = models.TextField(max_length=1000, verbose_name="Контент")
    status = models.ForeignKey('webapp.StatusModel', null=True, blank=True, on_delete=models.CASCADE,
                               related_name='statuses', verbose_name='Статусы')
    type = models.ManyToManyField('webapp.TypeModel', blank=True, related_name='types',
                                  verbose_name='Типы')
    project = models.ForeignKey('webapp.ProjectModel', on_delete=models.CASCADE,
                                related_name='tasks', verbose_name='Проекты')

    def __str__(self):
        return f"{self.pk}, {self.title}, {self.content}, {self.status}"

    def get_absolute_url(self):
        return reverse('task_view', kwargs={'pk': self.pk})

    class Meta:
        db_table = "issue"
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"


class ProjectModel(models.Model):
    title = models.CharField(max_length=50, verbose_name="Краткое описание")
    content = models.TextField(max_length=1000, verbose_name="Контент")
    created_at = models.DateField(verbose_name='Дата создания')
    updated_at = models.DateField(null=True, blank=True, verbose_name='Дата изменения')

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('project_view', kwargs={'pk': self.pk})

    class Meta:
        db_table = "products"
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"