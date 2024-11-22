from rest_framework import generics, mixins, status
from rest_framework.response import Response
from ..serializers.user import UserSerializer
from ..models.user import User


class SignupView(mixins.CreateModelMixin, generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            return Response(
                {
                    "message":"회원가입 성공",
                    # "id":user.username,
                    # "nickname":user.nickname,
                    # "email":user.email,
                    # "major":user.major,
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)