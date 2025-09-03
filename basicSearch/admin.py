from django.contrib import admin
from .models import Restaurant

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'neighbourhood', 'reservation_partner', 'rating', 'price_range')
    list_filter = ('reservation_partner', 'rating', 'price_range', 'neighbourhood')
    search_fields = ('name', 'address', 'neighbourhood', 'cuisine')
    ordering = ('-rating', 'name')
    
    fieldsets = (
        ('Core Information', {
            'fields': ('name', 'place_id', 'address', 'neighbourhood', 'cuisine')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Contact & Links', {
            'fields': ('website', 'phone', 'menu_url')
        }),
        ('Reservations', {
            'fields': ('reservation_url', 'reservation_partner')
        }),
        ('Social Media', {
            'fields': ('instagram_url', 'facebook_url', 'x_url', 'tiktok_url')
        }),
        ('Classification', {
            'fields': ('rating', 'price_range', 'vibes')
        }),
        ('Media', {
            'fields': ('images', 'operating_hours')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('id', 'created_at', 'updated_at')
