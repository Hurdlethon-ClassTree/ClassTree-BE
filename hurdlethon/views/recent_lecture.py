from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Max

from ..models.lecture import Lecture
from ..serializers.lecture import LectureSerializer  # 강의 정보를 반환하는 Serializer

class RecentQuestionLectureView(generics.ListAPIView):
    """
    최근에 질문이 올라온 강의 목록을 반환하는 API
    """
    serializer_class = LectureSerializer

    def get_queryset(self):
        """
        가장 최근 질문이 올라온 강의를 반환
        """
        # 각 강의의 가장 최신 질문을 기준으로 정렬
        lectures_with_latest_question = (
            Lecture.objects
            .annotate(latest_question_created_at=Max('questions__created_at'))  # 질문의 최신 날짜를 기준으로 정렬
            .filter(latest_question_created_at__isnull=False)  # 질문이 있는 강의만 필터링
            .order_by('-latest_question_created_at')[:10]  # 최근 10개의 강의만 반환
        )
        return lectures_with_latest_question

    def list(self, request, *args, **kwargs):
        """
        최근 질문이 올라온 강의 목록 반환
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
