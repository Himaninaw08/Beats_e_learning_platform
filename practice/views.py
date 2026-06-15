from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone

from .models import PracticeVideo, PracticeProgress, StudentPracticeUpload,Homework,HomeworkSubmission
from courses.models import CourseBooking
from .serializers import (
    PracticeVideoSerializer,
    TeacherUploadLessonVideoSerializer,
    StudentPracticeUploadSerializer,
    HomeworkSerializer,
    HomeworkSubmissionSerializer,
    # PracticeNoteSerializer
    

)
from beats_academy.utils import api_response
from beats_academy.utils import custom_exception_handler 


class TeacherUploadLessonVideoView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        if request.user.role not in ['teacher', 'admin']:

            return api_response(
                False,
                "Only teachers or admins can upload lesson videos",
                None,
                status.HTTP_403_FORBIDDEN
            )

        serializer = TeacherUploadLessonVideoSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                uploaded_by=request.user
            )

            return api_response(
                True,
                "Lesson video uploaded successfully",
                serializer.data,
                status.HTTP_201_CREATED
            )

        return api_response(
            False,
            "Invalid data",
            serializer.errors,
            status.HTTP_400_BAD_REQUEST
        )


class PracticeVideoListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        course_id = request.query_params.get('course_id')

        if not course_id:

            return api_response(
                False,
                "course_id is required",
                None,
                status.HTTP_400_BAD_REQUEST
            )

        videos = PracticeVideo.objects.filter(
            course_id=course_id
        ).order_by('order')

        serializer = PracticeVideoSerializer(
            videos,
            many=True,
            context={'request': request}
        )

        return api_response(
            True,
            "Practice videos fetched successfully",
            serializer.data,
            status.HTTP_200_OK
        )


class PracticeVideoDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, video_id):

        try:
            video = PracticeVideo.objects.get(id=video_id)

        except PracticeVideo.DoesNotExist:

            return api_response(
                False,
                "Video not found",
                None,
                status.HTTP_404_NOT_FOUND
            )

        serializer = PracticeVideoSerializer(
            video,
            context={'request': request}
        )

        return api_response(
            True,
            "Video fetched successfully",
            serializer.data,
            status.HTTP_200_OK
        )


class MarkVideoCompleteView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, video_id):

        try:
            video = PracticeVideo.objects.get(id=video_id)

        except PracticeVideo.DoesNotExist:

            return api_response(
                False,
                "Video not found",
                None,
                status.HTTP_404_NOT_FOUND
            )

        progress, created = PracticeProgress.objects.get_or_create(
            student=request.user,
            video=video
        )

        progress.is_completed = True
        progress.completed_at = timezone.now()
        progress.save()

        return api_response(
            True,
            "Marked as completed",
            None,
            status.HTTP_200_OK
        )


class UploadPracticeVideoView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, video_id):

        try:
            video = PracticeVideo.objects.get(id=video_id)

        except PracticeVideo.DoesNotExist:

            return api_response(
                False,
                "Lesson video not found",
                None,
                status.HTTP_404_NOT_FOUND
            )

        progress = PracticeProgress.objects.filter(
            student=request.user,
            video=video,
            is_completed=True
        ).exists()

        if not progress:

            return api_response(
                False,
                "Please mark the lesson as complete before uploading",
                None,
                status.HTTP_400_BAD_REQUEST
            )

        serializer = StudentPracticeUploadSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                student=request.user,
                video=video
            )

            return api_response(
                True,
                "Practice video uploaded successfully",
                serializer.data,
                status.HTTP_201_CREATED
            )

        return api_response(
            False,
            "Invalid data",
            serializer.errors,
            status.HTTP_400_BAD_REQUEST
        )



class HomeworkListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        # automatically find student's course from their booking
        booking = CourseBooking.objects.filter(
            student=request.user,
            status='confirmed'
        ).first()

        if not booking:
            return api_response(
                False,
                "No active booking found",
                None,
                status.HTTP_404_NOT_FOUND
            )

        # get all homework for their course
        homework_list = Homework.objects.filter(
            video__course=booking.course
        ).order_by('-created_at')

        total = homework_list.count()

        completed = HomeworkSubmission.objects.filter(
            student=request.user,
            homework__in=homework_list,
            status__in=['submitted', 'approved']
        ).count()

        serializer = HomeworkSerializer(
            homework_list,
            many=True,
            context={'request': request}
        )

        return api_response(
            True,
            "Homework fetched successfully",
            {
                "progress": {
                    "completed": completed,
                    "total": total,
                    "percentage": int((completed / total) * 100) if total > 0 else 0
                },
                "homework_list": serializer.data
            },
            status.HTTP_200_OK
        )

# POST: student uploads practice video for homework
class UploadHomeworkPracticeVideoView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, homework_id):

        try:
            homework = Homework.objects.get(id=homework_id)

        except Homework.DoesNotExist:

            return api_response(
                False,
                "Homework not found",
                None,
                status.HTTP_404_NOT_FOUND
            )

        submission, created = HomeworkSubmission.objects.get_or_create(
            student=request.user,
            homework=homework
        )

        # save the uploaded practice video
        practice_video = request.FILES.get('practice_video')

        if not practice_video:

            return api_response(
                False,
                "Practice video is required",
                None,
                status.HTTP_400_BAD_REQUEST
            )

        submission.practice_video = practice_video
        submission.save()

        return api_response(
            True,
            "Practice video uploaded successfully",
            None,
            status.HTTP_200_OK
        )


# POST: student submits homework (only after uploading practice video)
class SubmitHomeworkView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, homework_id):

        try:
            homework = Homework.objects.get(id=homework_id)

        except Homework.DoesNotExist:

            return api_response(
                False,
                "Homework not found",
                None,
                status.HTTP_404_NOT_FOUND
            )

        try:
            submission = HomeworkSubmission.objects.get(
                student=request.user,
                homework=homework
            )

        except HomeworkSubmission.DoesNotExist:

            return api_response(
                False,
                "Please upload your practice video first",
                None,
                status.HTTP_400_BAD_REQUEST
            )

        # check if practice video uploaded
        if not submission.practice_video:

            return api_response(
                False,
                "Please upload your practice video before submitting",
                None,
                status.HTTP_400_BAD_REQUEST
            )

        # check if already submitted
        if submission.status == 'submitted':

            return api_response(
                False,
                "Homework already submitted - waiting for review",
                None,
                status.HTTP_400_BAD_REQUEST
            )

        # check if already approved
        if submission.status == 'approved':

            return api_response(
                False,
                "Homework already approved by teacher",
                None,
                status.HTTP_400_BAD_REQUEST
            )

        submission.status = 'submitted'
        submission.save()

        return api_response(
            True,
            "Homework submitted successfully",
            None,
            status.HTTP_200_OK
        )


# POST: teacher approves or rejects homework (teacher/admin only)
class ReviewHomeworkView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, submission_id):

        # only teacher or admin can review
        if request.user.role not in ['teacher', 'admin']:

            return api_response(
                False,
                "Only teachers can review homework",
                None,
                status.HTTP_403_FORBIDDEN
            )

        try:
            submission = HomeworkSubmission.objects.get(id=submission_id)

        except HomeworkSubmission.DoesNotExist:

            return api_response(
                False,
                "Submission not found",
                None,
                status.HTTP_404_NOT_FOUND
            )

        review_status = request.data.get('status')   # 'approved' or 'rejected'
        teacher_reply = request.data.get('teacher_reply', '')

        if review_status not in ['approved', 'rejected']:

            return api_response(
                False,
                "Status must be approved or rejected",
                None,
                status.HTTP_400_BAD_REQUEST
            )

        submission.status = review_status
        submission.teacher_reply = teacher_reply
        submission.save()

        return api_response(
            True,
            f"Homework {review_status} successfully",
            None,
            status.HTTP_200_OK
        )