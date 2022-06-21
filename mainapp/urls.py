from django.urls import path

from mainapp import views
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    # Main
    path('', views.MainPageView.as_view(), name='index'),

    # News
    path('news/', views.NewsListView.as_view(), name='news'),
    path('news/add/', views.NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/update/', views.NewsUpdateView.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),
    path('news/<int:pk>/detail/', views.NewsPageDetailViews.as_view(), name='news_detail'),

    # Courses
    path('courses/', views.CoursesListView.as_view(), name='courses'),
    path('courses/<int:pk>/detail/', views.CoursesDetailView.as_view(), name='courses_detail'),
    path('courses/feedback/', views.CourseFeedbackCreateView.as_view(), name='course_feedback'),

    # Else
    path('contacts/', views.ContactsPageView.as_view(), name='contacts'),
    path('doc_site/', views.DocSitePageView.as_view(), name='doc_site'),
    path('login/', views.LoginPageView.as_view(), name='login'),

]
