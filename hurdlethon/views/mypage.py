import json

from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from hurdlethon.models import Lecture
from hurdlethon.serializers.mypage import MypageUpdateSerializer
from hurdlethon.serializers.user import UserSerializer


class MypageView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        user.interests=user.get_interests()
        return user