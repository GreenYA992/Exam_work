# noinspection PyUnresolvedReferences
from django.shortcuts import render, get_object_or_404
# noinspection PyUnresolvedReferences
from django.contrib.auth.decorators import login_required
# noinspection PyUnresolvedReferences
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# noinspection PyUnresolvedReferences
from django.db.models import Q
from .models import User, UserPhoto


def home(request):
    """Главная страница с поиском и фильтрацией"""
    # Получаем всех активных пользователей
    users_list = User.objects.filter(is_active=True).order_by('-created_at')

    # Параметры поиска из GET-запроса
    search_query = request.GET.get('search', '')
    gender_filter = request.GET.get('gender', '')
    city_filter = request.GET.get('city', '')
    age_min = request.GET.get('age_min', '')
    age_max = request.GET.get('age_max', '')
    status_filter = request.GET.get('status', '')

    # Применяем фильтры
    if search_query:
        users_list = users_list.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(hobbies__icontains=search_query)
        )

    if gender_filter:
        users_list = users_list.filter(gender=gender_filter)

    if city_filter:
        users_list = users_list.filter(city__icontains=city_filter)

    if age_min:
        users_list = users_list.filter(age__gte=age_min)

    if age_max:
        users_list = users_list.filter(age__lte=age_max)

    if status_filter:
        users_list = users_list.filter(status=status_filter)

    # Пагинация - 10 пользователей на страницу
    paginator = Paginator(users_list, 10)
    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    # Получаем главные фото для каждого пользователя
    for user in users:
        user.main_photo = UserPhoto.objects.filter(
            user=user,
            is_main=True
        ).first()

    # Уникальные города для фильтра
    cities = User.objects.filter(is_active=True).values_list(
        'city', flat=True
    ).distinct().order_by('city')

    context = {
        'users': users,
        'search_query': search_query,
        'gender_filter': gender_filter,
        'city_filter': city_filter,
        'age_min': age_min,
        'age_max': age_max,
        'status_filter': status_filter,
        'cities': cities,
        'genders': User.GENDER_CHOICES,
        'statuses': User.STATUS_CHOICES,
    }

    return render(request, 'dating/home.html', context)


@login_required
def user_detail(request, user_id):
    """Детальная страница пользователя"""
    user = get_object_or_404(User, id=user_id, is_active=True)
    photos = UserPhoto.objects.filter(user=user)
    main_photo = photos.filter(is_main=True).first()

    context = {
        'profile_user': user,
        'photos': photos,
        'main_photo': main_photo,
    }

    return render(request, 'dating/user_detail.html', context)
