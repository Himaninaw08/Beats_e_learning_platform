from django.urls import path
from .views import MyNotificationsView, MarkAsReadView

urlpatterns = [
    path('my-notifications/', MyNotificationsView.as_view()),
    path('notifications/<int:pk>/read/', MarkAsReadView.as_view()),
]