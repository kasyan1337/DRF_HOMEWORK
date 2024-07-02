
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonDetailView, LessonListCreateAPIView

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonListCreateAPIView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('courses/<int:course_pk>/lessons/', LessonListCreateAPIView.as_view(), name='lesson-list-create'),
    path('courses/<int:course_pk>/lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
]
