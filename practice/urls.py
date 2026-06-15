from django.urls import path
from .views import (
    TeacherUploadLessonVideoView,
    PracticeVideoListView,
    PracticeVideoDetailView,
    MarkVideoCompleteView,
    UploadPracticeVideoView,
    HomeworkListView,
    UploadHomeworkPracticeVideoView,
    SubmitHomeworkView,
    ReviewHomeworkView
    # PracticeNoteListView
)

urlpatterns = [

    # teacher/admin uploads lesson video
    path(
        'lesson/upload/',
        TeacherUploadLessonVideoView.as_view(),
        name='teacher-upload-lesson'
    ),

    # student gets list of all lesson videos for a course
    path(
        'videos/',
        PracticeVideoListView.as_view(),
        name='practice-video-list'
    ),

    # student gets single lesson video detail
    path(
        'videos/<int:video_id>/',
        PracticeVideoDetailView.as_view(),
        name='practice-video-detail'
    ),

    # student marks lesson video as complete
    path(
        'videos/<int:video_id>/complete/',
        MarkVideoCompleteView.as_view(),
        name='mark-video-complete'
    ),

    # student uploads their own practice video
    path(
        'videos/<int:video_id>/upload/',
        UploadPracticeVideoView.as_view(),
        name='upload-practice-video'
    ),

     # homework
    path('homework/', HomeworkListView.as_view()),
    path('homework/<int:homework_id>/upload-practice/', UploadHomeworkPracticeVideoView.as_view()),
    path('homework/<int:homework_id>/submit/', SubmitHomeworkView.as_view()),
    path('homework/review/<int:submission_id>/', ReviewHomeworkView.as_view()),

    # # notes
    # path('notes/', PracticeNoteListView.as_view()),
]