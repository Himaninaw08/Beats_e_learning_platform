from django.urls import path

from .views import (
    CourseListView,
    CourseDetailView,
    DemoSlotListView,
    BookClassView,
    CourseBookingDetailView,
    CreatePaymentView,
    PaymentDetailView,
    BookingFeeStatusView,
)

urlpatterns = [

    path(
        '',
        CourseListView.as_view(),
        name='course-list'
    ),

    path(
        '<int:pk>/',
        CourseDetailView.as_view(),
        name='course-detail'
    ),

    path(
        'teachers/<int:course_id>/slots/',
        DemoSlotListView.as_view(),
        name='demo-slots'
    ),

    path(
        'book-demo/',
        BookClassView.as_view(),
        name='book-demo'
    ),

    path(
        'demo-booking/<int:booking_id>/',
        CourseBookingDetailView.as_view()
    ),

    path(
    'payments/create/',
    CreatePaymentView.as_view()
    ),

    path(
    'payments/<int:payment_id>/',
        PaymentDetailView.as_view()
    ),  

    path('booking/<int:booking_id>/fee-status/', BookingFeeStatusView.as_view()),
]