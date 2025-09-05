# noinspection PyUnresolvedReferences
from django.contrib import admin
# noinspection PyUnresolvedReferences
from django.contrib.auth.admin import UserAdmin
# noinspection PyUnresolvedReferences
from django.utils.html import format_html
from .models import User, UserPhoto, UserInteraction, Match, ContactExchange


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'age', 'city',
                    'gender', 'status', 'likes_count', 'is_private', 'is_active')
    list_filter = ('gender', 'status', 'is_private', 'is_active', 'city', 'created_at')
    search_fields = ('email', 'first_name', 'last_name', 'city')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'likes_count')

    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'gender', 'age', 'city', 'hobbies')
        }),
        ('Статус и настройки', {
            'fields': ('status', 'likes_count', 'is_private')
        }),
        ('Разрешения', {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions')
        }),
        ('Важные даты', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',
                       'first_name', 'last_name', 'gender', 'age', 'city'),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()




class UserPhotoInline(admin.TabularInline):
    model = UserPhoto
    extra = 1
    readonly_fields = ('preview_photo', 'uploaded_at')

    def preview_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" height="100" />', obj.photo.url)
        return "Нет фото"

    preview_photo.short_description = 'Предпросмотр'


@admin.register(UserPhoto)
class UserPhotoAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'preview_photo', 'is_main', 'uploaded_at')
    list_filter = ('is_main', 'uploaded_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('uploaded_at', 'preview_photo')
    list_editable = ('is_main',)

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'Email пользователя'
    user_email.admin_order_field = 'user__email'

    def preview_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" height="50" />', obj.photo.url)
        return "Нет фото"

    preview_photo.short_description = 'Фото'


@admin.register(UserInteraction)
class UserInteractionAdmin(admin.ModelAdmin):
    list_display = ('from_user_email', 'to_user_email', 'interaction_type', 'timestamp')
    list_filter = ('interaction_type', 'timestamp')
    search_fields = ('from_user__email', 'to_user__email')
    readonly_fields = ('timestamp',)

    def from_user_email(self, obj):
        return obj.from_user.email

    from_user_email.short_description = 'От пользователя'
    from_user_email.admin_order_field = 'from_user__email'

    def to_user_email(self, obj):
        return obj.to_user.email

    to_user_email.short_description = 'К пользователю'
    to_user_email.admin_order_field = 'to_user__email'


class ContactExchangeInline(admin.TabularInline):
    model = ContactExchange
    extra = 0
    readonly_fields = ('created_at', 'accepted_at')


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'users_list', 'created_at', 'last_interaction', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('users__email', 'users__first_name')
    readonly_fields = ('created_at', 'last_interaction')
    filter_horizontal = ('users',)
    inlines = [ContactExchangeInline]

    def users_list(self, obj):
        return ", ".join([user.email for user in obj.users.all()])

    users_list.short_description = 'Пользователи'


@admin.register(ContactExchange)
class ContactExchangeAdmin(admin.ModelAdmin):
    list_display = ('match_id', 'initiator_email', 'accepted', 'created_at')
    list_filter = ('accepted', 'created_at')
    readonly_fields = ('created_at', 'accepted_at')

    def match_id(self, obj):
        return f"Match #{obj.match.id}"

    match_id.short_description = 'Мэтч'
    match_id.admin_order_field = 'match__id'

    def initiator_email(self, obj):
        return obj.initiator.email

    initiator_email.short_description = 'Инициатор'
    initiator_email.admin_order_field = 'initiator__email'


# Кастомная настройка админки
admin.site.site_header = "Панель администратора Dating App"
admin.site.site_title = "Dating App Admin"
admin.site.index_title = "Управление приложением знакомств"


