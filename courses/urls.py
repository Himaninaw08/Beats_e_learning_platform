from django.urls import path

from .views import (
    CourseListView,
    CourseDetailView,
    DemoSlotListView,
    BookDemoClassView,
    DemoBookingDetailView
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
        'teachers/<int:teacher_id>/slots/',
        DemoSlotListView.as_view(),
        name='demo-slots'
    ),

    path(
        'book-demo/',
        BookDemoClassView.as_view(),
        name='book-demo'
    ),

    path(
        'demo-booking/<int:booking_id>/',
        DemoBookingDetailView.as_view()
    ),
]