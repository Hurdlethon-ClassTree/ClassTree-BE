from rest_framework import generics, mixins, status, serializers
from rest_framework.response import Response

from ..models import Lecture
from ..serializers.user import UserCreateSerializer
from ..models.user import User
import json


class SignupView(mixins.CreateModelMixin, generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserCreateSerializer

    def get_serializer_context(self):
        """
        강의 개수를 동적으로 확인해 선택 가능한 개수 제한.
        """
        lectures = Lecture.objects.all()
        return {"lectures": lectures}


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            user.total_point=100 # initial point
            user.save()
            return Response(
                {
                    "message":"회원가입 성공",
                    "username": user.username,
                    "initial_points": user.total_point,
                    "interests": json.loads(user.interests),

                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #[GET] /signup 시 강의목록 반환
    def get(self, request, *args, **kwargs):
        # 강의 선택을 위한 강의 목록 반환
        lectures = Lecture.objects.values('lecture_id', 'lecture_name')  # 강의 ID와 이름만 가져오기
        return Response(
            {
                "Valid Lectures": list(lectures)
            },
            status=status.HTTP_200_OK
        )