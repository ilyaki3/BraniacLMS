from django.contrib import admin

from mainapp.models import Course, CourseTeacher, News, Lesson

admin.site.register(Course)
admin.site.register(CourseTeacher)
admin.site.register(Lesson)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'deleted')
    list_filter = ('deleted', 'created')
    ordering = ('pk',)
    list_per_page = 10
    search_fields = ('title', 'preamble', 'body')
    actions = ('mark_as_delete',)


    def mark_as_delete(self, request, queryset):
        queryset.update(deleted=True)

    mark_as_delete.short_description = 'Пометить удаленным'
