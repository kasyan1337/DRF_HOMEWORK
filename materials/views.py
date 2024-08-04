# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscription
from materials.paginators import CustomPagination
from materials.serializers import LessonSerializer, CourseSerializer
from users.permissions import IsOwner, IsModerator


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsOwner, ~IsModerator]
        elif self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsOwner, ~IsModerator]
        elif self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)

        subs_items = Subscription.objects.filter(user=user, course=course_item)

        if subs_items.exists():
            subs_items.delete()
            message = "You have successfully unsubscribed from the course!"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "You have successfully subscribed to the course!"
        return Response({"message": message})
