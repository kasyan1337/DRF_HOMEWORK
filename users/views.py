from django_filters import rest_framework as filters
from rest_framework import generics, permissions, viewsets
from rest_framework.filters import OrderingFilter

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from users.models import Payment, User
from users.permissions import IsModerator, IsOwner
from users.serializers import PaymentSerializer, RegisterSerializer, UserSerializer


# Create your views here.


class PaymentFilter(filters.FilterSet):
    paid_course = filters.NumberFilter(field_name='paid_course__id')
    paid_lesson = filters.NumberFilter(field_name='paid_lesson__id')
    payment_method = filters.CharFilter(field_name='payment_method')

    class Meta:
        model = Payment
        fields = ['user', 'payment_date', 'paid_course', 'paid_lesson', 'amount', 'payment_method']


class PaymentListView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'partial_update']:
            self.permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser, IsModerator,
                                       IsOwner]
        elif self.action in ['create', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser, IsOwner]
        return [permission() for permission in self.permission_classes]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'partial_update']:
            self.permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser, IsModerator,
                                       IsOwner]
        elif self.action in ['create', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser, IsOwner]
        return [permission() for permission in self.permission_classes]
