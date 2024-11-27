from rest_framework import generics, permissions, serializers, status
from rest_framework.generics import ListAPIView
from django.db.models import Q
from rest_framework.response import Response

from .question import QuestionListCreateView
from ..models import Lecture
from ..models.question import Question
from ..serializers.lecture import LectureSerializer
from ..serializers.question import QuestionSerializer
from rest_framework.exceptions import NotFound

class LectureListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LectureSerializer
    # Serializer로 만들었습니다
    def get_queryset(self):
        return self.serializer_class.filter_queryset(self.request)

    def get(self,request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"lecture_list": serializer.data})

class LectureDetailView(ListAPIView):
    """
    Retrieves a lecture's details and its associated questions.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuestionSerializer

    def get_queryset(self):
        """
        Returns the queryset of questions associated with a specific lecture.
        """
        lecture_id = self.kwargs.get('pk')  # Get lecture ID from URL
        try:
            lecture = Lecture.objects.prefetch_related('questions').get(pk=lecture_id)
        except Lecture.DoesNotExist:
            raise NotFound({"detail": "Lecture not found."})  # Raise a 404 error if lecture is not found

        # Retrieve and filter questions related to this lecture
        queryset = lecture.questions.all()

        # Optional filtering based on query parameters
        checked = self.request.query_params.get('checked')
        curious_min = self.request.query_params.get('curious_min')
        point_min = self.request.query_params.get('point_min')
        sort_by = self.request.query_params.get('sort_by')

        # Apply filters
        if checked is not None:
            queryset = queryset.filter(checked=checked.lower() == 'true')  # Filter by 'checked'
        if curious_min is not None:
            queryset = queryset.filter(curious__gte=int(curious_min))  # Filter by curious >= minimum
        if point_min is not None:
            queryset = queryset.filter(point__gte=int(point_min))  # Filter by point >= minimum

        # Apply sorting
        if sort_by:
            queryset = queryset.order_by(sort_by)

        return queryset

    def list(self, request, *args, **kwargs):
        """
        Customizes the response to include lecture details and related questions.
        """
        # Fetch the lecture
        lecture_id = self.kwargs.get('pk')
        try:
            lecture = Lecture.objects.get(pk=lecture_id)
        except Lecture.DoesNotExist:
            return Response({"detail": "Lecture not found."}, status=404)

        # Serialize and include questions
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "lecture": LectureSerializer(lecture).data,
            "questions": serializer.data
        })