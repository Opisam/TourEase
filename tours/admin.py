from django.contrib import admin
from .models import TourPackage, BookingRequest, Review, Message


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'price', 'is_approved', 'is_active', 'created_at')
    list_filter = ('is_approved', 'is_active', 'tour_type', 'created_at')
    search_fields = ('title', 'location', 'company__username')
    actions = ['approve_tours', 'activate_tours', 'deactivate_tours']

    def approve_tours(self, request, queryset):
        queryset.update(is_approved=True)
    approve_tours.short_description = 'Approve selected tours'

    def activate_tours(self, request, queryset):
        queryset.update(is_active=True)
    activate_tours.short_description = 'Activate selected tours'

    def deactivate_tours(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_tours.short_description = 'Deactivate selected tours'


@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'travel_date', 'number_of_people', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'tour__title')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'tour__title')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__username', 'receiver__username', 'content')
