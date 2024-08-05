# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscription, Payment
from materials.paginators import CustomPagination
from materials.serializers import LessonSerializer, CourseSerializer
from materials.services import create_product, create_price, create_checkout_session
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


class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get('course_id')
        success_url = request.data.get('success_url')
        cancel_url = request.data.get('cancel_url')

        course = get_object_or_404(Course, id=course_id)

        if course.price <= 0:
            return Response({"error": "Course price must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)

        amount_in_cents = int(course.price * 100)

        product = create_product(course.title)
        price = create_price(product['id'], amount_in_cents)  # Amount in cents

        session = create_checkout_session(price['id'], success_url, cancel_url)

        Payment.objects.create(
            user=request.user,
            course=course,
            stripe_session_id=session['id'],
            amount=course.price
        )

        return Response(session, status=status.HTTP_201_CREATED)
