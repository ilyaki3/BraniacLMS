from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from mainapp.forms import CourseFeedbackForm
from mainapp.models import Lesson, CourseFeedback, CourseTeacher
from mainapp.models import News, Course


# Main Page
class MainPageView(TemplateView):
    template_name = 'mainapp/index.html'


# News
class NewsListView(ListView):
    model = News
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class NewsPageDetailViews(DetailView):
    model = News


class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = News
    fields = '__all__'
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.add_news',)


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = News
    fields = '__all__'
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.change_news',)


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.delete_news',)


# Courses
class CoursesListView(ListView):
    template_name = 'mainapp/course_list.html'
    model = Course


class CoursesDetailView(TemplateView):
    template_name = 'mainapp/courses_detail.html'

    def get_context_data(self, pk=None, **kwargs):
        context = super(CoursesDetailView, self).get_context_data(**kwargs)
        context['course_object'] = get_object_or_404(Course, pk=pk)
        context['lessons'] = Lesson.objects.filter(course=context['course_object'])
        context['teachers'] = CourseTeacher.objects.filter(course=context['course_object'])
        context['feedback_list'] = CourseFeedback.objects.filter(course=context['course_object'])

        if self.request.user.is_authenticated:
            context['feedback_form'] = CourseFeedbackForm(course=context['course_object'], user=self.request.user)

        return context


class CourseFeedbackCreateView(CreateView):
    model = CourseFeedback
    form_class = CourseFeedbackForm

    def form_valid(self, form):
        self.object = form.save()
        rendered_template = render_to_string('mainapp/includes/feedback_card.html', context={'item': self.object})
        return JsonResponse({'card': rendered_template})


# Contacts
class ContactsPageView(TemplateView):
    template_name = 'mainapp/contacts.html'


# DocSite

class DocSitePageView(TemplateView):
    template_name = 'mainapp/doc_site.html'


# Login

class LoginPageView(TemplateView):
    template_name = 'authapp/login.html'
