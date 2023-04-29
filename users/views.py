from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework import permissions
from rest_framework.response import Response
from users.serializers import (
    UserSerializer,
    CustomTokenObtainPairSerializer,
    UserUpdateSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User
from django.contrib import auth


# Create your views here.
class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"회원가입 성공!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"massage": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST
            )


class ProfileView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            serializer = UserUpdateSerializer(user)
            return Response(serializer.data)
        else:
            return Response({"권한이 없습니다!"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"권한이 없습니다!"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            serializer = UserSerializer(user, data=request.data)
            user.delete()
            return Response({"회원탈퇴 완료!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"권한이 없습니다"}, status=status.HTTP_403)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class mockView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        print(request.user)
        return Response("로그인중!")
