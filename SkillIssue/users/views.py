from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from rest_framework import status, permissions, generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import UserProfile, Review, Guide, GuideRating
from .serializers import RegisterSerializer, UserProfileSerializer, ReviewSerializer, GuideSerializer
from .forms import GuideForm


def main_page(request):
    return render(request, "users/main.html")


def register_page(request):
    return render(request, "users/reg.html")


def login_page(request):
    return render(request, "users/log.html")


def profile_page(request, username):
    user_obj = get_object_or_404(User, username=username)
    profile = user_obj.profile
    guides = Guide.objects.filter(author=user_obj).order_by('-created_at')
    reviews = Review.objects.filter(profile=profile).order_by('-created_at')

    return render(request, "users/profile.html", {
        "username": username,
        "profile": profile,
        "guides": guides,
        "reviews": reviews
    })


def logout_view(request):
    logout(request)
    return redirect("main_page")


def profile_guides_api(username):
    user_obj = get_object_or_404(User, username=username)
    guides = Guide.objects.filter(author=user_obj).order_by('-created_at')
    guides_data = [
        {
            "id": g.id,
            "title": g.title,
            "image": g.image.url if g.image else None,
            "created_at": g.created_at,
        }
        for g in guides
    ]
    return JsonResponse({"guides": guides_data})


@login_required
def guides_list(request):
    guides = Guide.objects.all().order_by('-rating', '-created_at')
    popular_guides = guides[:6]
    top_guides = guides.order_by('-rating')[:6]
    return render(request, 'users/guides.html', {
        'popular_guides': popular_guides,
        'top_guides': top_guides
    })


@login_required
def guides_search(request):
    query = request.GET.get('query', '')
    tags_input = request.GET.get('tags', '')
    guides = Guide.objects.all()

    if query:
        guides = guides.filter(title__icontains=query)

    if tags_input:
        tags_list = [t.strip() for t in tags_input.split(',') if t.strip()]
        for tag in tags_list:
            guides = guides.filter(tags__icontains=tag)

    return render(request, 'users/guides_search_res.html', {'guides': guides})


@login_required
def create_guide(request):
    if request.method == 'POST':
        form = GuideForm(request.POST, request.FILES)
        if form.is_valid():
            guide = form.save(commit=False)
            guide.author = request.user
            if isinstance(guide.tags, str):
                guide.tags = [tag.strip() for tag in guide.tags.split(',') if tag.strip()]
            guide.save()
            return redirect('guides_list')
    else:
        form = GuideForm()
    return render(request, 'users/create_guides.html', {'form': form})


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
            return Response({"error": "Введите логин и пароль"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({"error": "Неверные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        response = Response({
            "message": "ok",
            "username": user.username,
            "csrf": get_token(request),
        })
        return response


class CurrentUserView(APIView):
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


class UserProfileDetailView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        username = self.kwargs.get("username")
        return get_object_or_404(UserProfile, user__username=username)


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        profile_id = self.request.data.get("profile_id")
        profile = get_object_or_404(UserProfile, id=profile_id)
        serializer.save(author=self.request.user, profile=profile)


class GuideViewSet(viewsets.ModelViewSet):
    queryset = Guide.objects.all().order_by('-rating', '-created_at')
    serializer_class = GuideSerializer


class GuideCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GuideSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)