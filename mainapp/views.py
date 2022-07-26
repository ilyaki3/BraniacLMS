from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.http import JsonResponse, FileResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from mainapp import tasks
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

        feedback_list_key = f'course_feedback_{context["course_object"].pk}'
        cashed_feedback_list = cache.get(feedback_list_key)
        if cashed_feedback_list is None:
            context['feedback_list'] = CourseFeedback.objects.filter(course=context['course_object'])
            cache.set(feedback_list_key, context['feedback_list'], timeout=300)
        else:
            context['feedback_list'] = cashed_feedback_list

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

    def post(self, *args, **kwargs):
        message_body = self.request.POST.get('message_body')
        message_from = self.request.user.pk if self.request.user.is_authenticated else None
        tasks.send_feedback_mail.delay(message_body, message_from)
        return HttpResponseRedirect(reverse_lazy("mainapp:contacts"))


# DocSite

class DocSitePageView(TemplateView):
    template_name = 'mainapp/doc_site.html'


# Login

class LoginPageView(TemplateView):
    template_name = 'authapp/login.html'


# Log

class LogView(UserPassesTestMixin, TemplateView):
    template_name = 'mainapp/logs.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        log_lines = []
        with open(settings.BASE_DIR / 'log/main_log.log') as log_file:
            for i, line in enumerate(log_file):
                if i == 1000:
                    break
                log_lines.insert(0, line)
        context_data['logs'] = log_lines
        return context_data


class LogDownloadView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        return FileResponse(open(settings.LOG_FILE, 'rb'))
