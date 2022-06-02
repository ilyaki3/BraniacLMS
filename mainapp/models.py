from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Edited", editable=False)
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
        return super().get_queryset().filter(deleted=False)


class News(BaseModel):
    objects = NewsManager()
    title = models.CharField(max_length=256, verbose_name="Title")
    preamble = models.CharField(max_length=1024, verbose_name="Preamble")
    body = models.TextField(blank=True, null=True, verbose_name="Body")
    body_as_markdown = models.BooleanField(default=False, verbose_name="As markdown")

    def __str__(self) -> str:
        return f"{self.pk} | {self.title}"

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = "новости"


class Course(BaseModel):
    name = models.CharField(max_length=256, verbose_name="Name")
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    description_as_markdown = models.BooleanField(default=False, verbose_name="As markdown")
    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Cost", default=0)
    cover = models.CharField(max_length=25, default="no_image.svg", verbose_name="Cover")

    def __str__(self) -> str:
        return f"{self.pk} {self.name}"

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    num = models.PositiveIntegerField(verbose_name="Lesson number")
    title = models.CharField(max_length=256, verbose_name="Title")
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    description_as_markdown = models.BooleanField(default=False, verbose_name="As markdown")

    def __str__(self) -> str:
        return f"{self.course.name} | {self.num} | {self.title}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        ordering = ("course", "num")


class CourseTeacher(BaseModel):
    course = models.ManyToManyField(Course)
    name_first = models.CharField(max_length=128, verbose_name="Name")
    name_second = models.CharField(max_length=128, verbose_name="Surname")
    day_birth = models.DateTimeField(verbose_name="Birth date")

    def __str__(self):
        return f"{self.pk} | {self.name_second} | {self.name_first}"

    class Meta:
        verbose_name = "учитель"
        verbose_name_plural = "учителя"
