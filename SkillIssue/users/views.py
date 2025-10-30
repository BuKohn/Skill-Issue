import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from rest_framework import status, permissions, generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
import markdown
from django.db.models import Avg
from django.utils.safestring import mark_safe


from .models import Profile, GuideRating as Review, Guide
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
    reviews = Review.objects.filter(guide__author=user_obj).order_by('-created_at')

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
    guide_id = request.GET.get('id')
    guide = None
    if guide_id:
        guide = get_object_or_404(Guide, id=guide_id)
        if guide.author != request.user:
            return redirect('guides_list')

    if request.method == 'POST':
        form = GuideForm(request.POST, request.FILES, instance=guide)
        if form.is_valid():
            guide_obj = form.save(commit=False)
            guide_obj.author = request.user
            guide_obj.save()

            content = guide_obj.content

            for key, file in request.FILES.items():
                if key.startswith('image_'):
                    from django.core.files.storage import default_storage
                    from django.core.files.base import ContentFile

                    filename = default_storage.save(f'guides/{file.name}', ContentFile(file.read()))
                    file_url = default_storage.url(filename)

                    content = content.replace(f'({file.name})', f'({file_url})')
                    content = content.replace(f'(1761295916746_{file.name})', f'({file_url})')

            guide_obj.content = content
            guide_obj.save()
            return redirect('guide_detail', pk=guide_obj.id)
    else:
        form = GuideForm(instance=guide)

    return render(request, 'users/create_guides.html', {'form': form, 'guide': guide})


def guide_detail(request, pk):
    guide = get_object_or_404(Guide, pk=pk)

    html = markdown.markdown(guide.content or "", extensions=['extra'])

    html = re.sub(
        r'<img\s+[^>]*src="(?!https?://|/|/media/)([^"]+)"',
        r'<img src="/media/guides/\1"',
        html
    )

    guide_content_html = mark_safe(html)
    reviews = guide.reviews.all()

    return render(request, 'users/guide_detail.html', {
        'guide': guide,
        'guide_content_html': guide_content_html,
        'reviews': reviews,
    })


@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        description = request.POST.get("description", "").strip()
        avatar = request.FILES.get("avatar")

        if username:
            request.user.username = username
            request.user.save()

        profile.bio = description
        if avatar:
            profile.avatar = avatar
        profile.save()

        return redirect(f"{request.path}?updated=1")

    return render(request, "users/profile_edit.html", {"profile": profile, "user": request.user})


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
        return get_object_or_404(Profile, user__username=username)


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        profile_id = self.request.data.get("profile_id")
        profile = get_object_or_404(Profile, id=profile_id)
        serializer.save(author=self.request.user, profile=profile)


class GuideCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GuideSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class GuideViewSet(viewsets.ModelViewSet):
    queryset = Guide.objects.all().order_by('-rating', '-created_at')
    serializer_class = GuideSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GuideRateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, guide_id):
        guide = get_object_or_404(Guide, id=guide_id)
        rating_value = int(request.data.get('rating', 0))

        if not 1 <= rating_value <= 5:
            return Response({'error': 'Рейтинг должен быть от 1 до 5'}, status=400)

        GuideRating.objects.update_or_create(
            guide=guide,
            reviewer=request.user,
            defaults={'rating': rating_value}
        )

        avg_guide_rating = guide.ratings.aggregate(avg=Avg('rating'))['avg'] or 0
        guide.rating = int(round(avg_guide_rating))
        guide.save(update_fields=['rating'])

        author_avg_rating = Guide.objects.filter(author=guide.author).aggregate(avg=Avg('rating'))['avg'] or 0
        profile = guide.author.profile
        profile.rating = int(round(author_avg_rating))
        print(profile.rating)
        profile.save(update_fields=['rating'])

        return Response({
            "guide_average_rating": guide.rating,
            "profile_average_rating": profile.rating
        })
