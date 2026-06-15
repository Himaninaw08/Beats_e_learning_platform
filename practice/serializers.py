from rest_framework import serializers
from .models import PracticeVideo, PracticeProgress, StudentPracticeUpload,Homework, HomeworkSubmission


class PracticeVideoSerializer(serializers.ModelSerializer):

    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = PracticeVideo
        fields = [
            'id',
            'title',
            'description',
            'video_file',
            'duration',
            'order',
            'is_completed'
        ]

    def get_is_completed(self, obj):

        request = self.context.get('request')

        if not request:
            return False

        progress = PracticeProgress.objects.filter(
            student=request.user,
            video=obj
        ).first()

        return progress.is_completed if progress else False


class TeacherUploadLessonVideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PracticeVideo
        fields = [
            'id',
            'course',
            'title',
            'description',
            'video_file',
            'duration',
            'order'
        ]


class StudentPracticeUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentPracticeUpload
        fields = [
            'id',
            'title',
            'level',
            'description',
            'video_file',
            'uploaded_at'
        ]

    



class HomeworkSerializer(serializers.ModelSerializer):

    submission_status = serializers.SerializerMethodField()
    teacher_reply = serializers.SerializerMethodField()
    has_uploaded_practice = serializers.SerializerMethodField()

    class Meta:
        model = Homework
        fields = [
            'id',
            'title',                  # card title
            'assignment_number',       # Assignment #1
            'instructions',            # instructions text
            'reference_video_url',     # Watch Reference Video button
            'due_date',               # Due Date
            'submission_status',       # pending/submitted/approved/rejected
            'teacher_reply',           # teacher feedback
            'has_uploaded_practice',   # whether student uploaded practice video
            'created_at'
        ]

    def get_submission_status(self, obj):

        request = self.context.get('request')

        submission = HomeworkSubmission.objects.filter(
            student=request.user,
            homework=obj
        ).first()

        return submission.status if submission else 'pending'

    def get_teacher_reply(self, obj):

        request = self.context.get('request')

        submission = HomeworkSubmission.objects.filter(
            student=request.user,
            homework=obj
        ).first()

        return submission.teacher_reply if submission else None

    def get_has_uploaded_practice(self, obj):

        request = self.context.get('request')

        submission = HomeworkSubmission.objects.filter(
            student=request.user,
            homework=obj
        ).first()

        if not submission:
            return False

        return bool(submission.practice_video)


class HomeworkSubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = HomeworkSubmission
        fields = [
            'id',
            'practice_video',
            'note',
            'status',
            'teacher_reply',
            'submitted_at'
        ]