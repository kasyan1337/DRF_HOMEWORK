from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import generics, permissions, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from materials.models import Course, Subscription
from users.models import Payment, User
from users.serializers import PaymentSerializer, RegisterSerializer, UserSerializer


# Create your views here.


class PaymentFilter(filters.FilterSet):
    paid_course = filters.NumberFilter(field_name="paid_course__id")
    paid_lesson = filters.NumberFilter(field_name="paid_lesson__id")
    payment_method = filters.CharFilter(field_name="payment_method")

    class Meta:
        model = Payment
        fields = [
            "user",
            "payment_date",
            "paid_course",
            "paid_lesson",
            "amount",
            "payment_method",
        ]


class PaymentListView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ["payment_date"]
    permission_classes = [permissions.IsAuthenticated]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    permission_classes = [AllowAny]


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class SubscribeView(APIView):

    def post(self, request):
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        user = request.user

        subscription, created = Subscription.objects.get_or_create(user=user, course=course)

        if created:
            return Response({"message": "Subscribed successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Already subscribed."}, status=status.HTTP_200_OK)
