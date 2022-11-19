from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"), editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Edited"), editable=False)
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ("-created",)

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class NewsManager(models.Manager):
    def delete(self):
        pass

    def get_queryset(self):
        return super().get_queryset().filter()


class News(BaseModel):
    objects = NewsManager()
    title = models.CharField(max_length=256, verbose_name=_("Title"))
    preamble = models.CharField(max_length=1024, verbose_name=_("Preamble"))
    body = models.TextField(blank=True, null=True, verbose_name=_("Body"))
    body_as_markdown = models.BooleanField(default=False, verbose_name=_("As markdown"))

    def __str__(self) -> str:
        return f"{self.pk} | {self.title}"

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = "новости"


class CourseManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class Course(BaseModel):
    objects = CourseManager()
    name = models.CharField(max_length=256, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    description_as_markdown = models.BooleanField(default=False, verbose_name=_("As markdown"))
    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_("Cost"), default=0)
    cover = models.CharField(max_length=25, default="no_image.svg", verbose_name=_("Cover"))

    def __str__(self) -> str:
        return f"{self.pk} {self.name}"

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    num = models.PositiveIntegerField(verbose_name=_("Lesson number"))
    title = models.CharField(max_length=256, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    description_as_markdown = models.BooleanField(default=False, verbose_name=_("As markdown"))

    def __str__(self) -> str:
        return f"{self.course.name} | {self.num} | {self.title}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        ordering = ("course", "num")


class CourseTeacher(BaseModel):
    course = models.ManyToManyField(Course)
    name_first = models.CharField(max_length=128, verbose_name=_("Name"))
    name_second = models.CharField(max_length=128, verbose_name=_("Surname"))
    day_birth = models.DateTimeField(verbose_name=_("Birth date"))

    def __str__(self):
        return f"{self.pk} | {self.name_second} | {self.name_first}"

    class Meta:
        verbose_name = "учитель"
        verbose_name_plural = "учителя"


class CourseFeedback(BaseModel):
    RATINGS = (
        (5, '⭐⭐⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (3, '⭐⭐⭐'),
        (2, '⭐⭐'),
        (1, '⭐')
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=_('Курс'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    rating = models.SmallIntegerField(choices=RATINGS, default=5, verbose_name=_('Рейтинг'))
    feedback = models.TextField(verbose_name=_('Отзыв'), default=_('Без отзыва'))

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзыв на {self.course} от{self.user}'