from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.filters import OrderingFilter

from users.models import Payment
from users.serializers import PaymentSerializer


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
