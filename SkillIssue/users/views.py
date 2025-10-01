from django.shortcuts import render

from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer


def main_page(request):
    return render(request, "users/main.html")


def register_page(request):
    return render(request, "users/reg.html")


def login_page(request):
    return render(request, "users/log.html")


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Пользователь зарегистрирован", "id": user.id},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response({"error": "Необходим пароль и логин"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({"error": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_active:
            return Response({"error": "Аккаунт отключён"}, status=status.HTTP_403_FORBIDDEN)

        login(request, user)
        return Response({"message": "Вход выполнен", "username": user.username, "csrf": get_token(request)})


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "date_joined": user.date_joined,
        })
