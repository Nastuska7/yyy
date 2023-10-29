from django.contrib import admin
from django.utils.html import format_html
from .models import Advertisement
from django.conf import settings


# Register your models here.

class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'price', 'updated_date', 'created_date', 'auction', 'image', 'display_thumbnail_image']
    list_filter = ['auction', 'created_at']
    actions = ['make_auction_as_false', 'make_auction_as_true']
    fieldsets = (
        ('Общее: ', {
            'fields': ('title', 'description', 'image')
        }),
        ('Финансы: ', {
            'fields': ('price', 'auction'),
            'classes': ['collapse']
        })
    )

    @admin.action(description='Убрать возможность торга')  # декоратор, чтобы добавить собственное описание
    def make_auction_as_false(self, request, queryset):
        queryset.update(auction=False)

    @admin.action(description='Добавить возможность торга')  # декоратор, чтобы добавить собственное описание
    def make_auction_as_true(self, request, queryset):
        queryset.update(auction=True)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()

    def display_thumbnail_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        else:
            default_image_url = settings.STATIC_URL + 'img/Default.jpg'
            return format_html('<img src="{}" width="50" height="50" />', default_image_url)

    display_thumbnail_image.short_description = 'Thumbnail Image'


admin.site.register(Advertisement, AdvertisementAdmin)  # регистрируем нашу новую модель
