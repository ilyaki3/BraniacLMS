from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

import mainapp.models
from mainapp.models import News


class MainPageView(TemplateView):
    template_name = 'mainapp/index.html'


class NewsPageView(TemplateView):
    template_name = 'mainapp/news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = News.objects.all()[:5]
        return context


class NewsPageDetailViews(TemplateView):
    template_name = 'mainapp/news_detail.html'

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(pk=pk, **kwargs)
        context['news_object'] = get_object_or_404(mainapp.models.News, pk=pk)
        return context


class CoursesListView(TemplateView):
    template_name = 'mainapp/courses_list.html'

    def get_context_data(self, **kwargs):
        context = super(CoursesListView, self).get_context_data(**kwargs)
        context['objects'] = mainapp.models.Course.objects.all()[:7]
        return context


class CoursesDetailView(TemplateView):
    template_name = 'mainapp/courses_detail.html'

    def get_context_data(self, pk=None, **kwargs):
        context = super(CoursesDetailView, self).get_context_data(**kwargs)
        context['course_object'] = get_object_or_404(mainapp.models.Course, pk=pk)
        context['lessons'] = mainapp.models.Lesson.objects.filter(course=context['course_object'])
        context['teachers'] = mainapp.models.CourseTeacher.objects.filter(course=context['course_object'])
        return context


class ContactsPageView(TemplateView):
    template_name = 'mainapp/contacts.html'


class DocSitePageView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class LoginPageView(TemplateView):
    template_name = 'mainapp/../authapp/templates/authapp/login.html'
