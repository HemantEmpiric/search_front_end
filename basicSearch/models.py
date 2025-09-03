import uuid
from django.db import models

# Create your models here.

class Restaurant(models.Model):
    # Core identifiers
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    place_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    
    # Basic information
    name = models.CharField(max_length=200)
    address = models.TextField()
    neighbourhood = models.CharField(max_length=100, blank=True)
    
    # Location coordinates
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    # Contact and links
    website = models.URLField(blank=True)
    reservation_url = models.URLField(blank=True)
    menu_url = models.URLField(blank=True)
    
    # Social media
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    x_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)
    
    # Reservation partner
    RESERVATION_PARTNERS = [
        ('OpenTable', 'OpenTable'),
        ('SevenRooms', 'SevenRooms'),
        ('Tock', 'Tock'),
        ('Other', 'Other'),
        ('None', 'None'),
    ]
    reservation_partner = models.CharField(max_length=20, choices=RESERVATION_PARTNERS, default='None')
    
    # Operating hours
    operating_hours = models.JSONField(default=dict, blank=True)
    
    # Vibes classification
    VIBES_CHOICES = [
        ('aesthetic', 'aesthetic'),
        ('bar', 'bar'),
        ('brunch', 'brunch'),
        ('business', 'business'),
        ('casual', 'casual'),
        ('chic', 'chic'),
        ('clubesque', 'clubesque'),
        ('cozy', 'cozy'),
        ('crowded', 'crowded'),
        ('date', 'date'),
        ('dj', 'dj'),
        ('dogfriendly', 'dog friendly'),
        ('drinks', 'drinks'),
        ('fancy', 'fancy'),
        ('finedining', 'fine fining'),
        ('foodexperience', 'food experience'),
        ('intimate', 'intimate'),
        ('largegroups', 'large groups'),
        ('largespace', 'large space'),
        ('liveevents', 'live events'),
        ('livemusic', 'live music'),
        ('loud', 'loud'),
        ('michelin', 'michelin'),
        ('notcrowded', 'not crowded'),
        ('patio', 'patio'),
        ('pool', 'pool'),
        ('privatedining', 'private dining'),
        ('quiet', 'quiet'),
        ('rooftop', 'rooftop'),
        ('shareable', 'shareable'),
        ('smallgroups', 'small groups'),
        ('smallplates', 'small plates'),
        ('smallspace', 'small space'),
        ('snacks', 'snacks'),
        ('speakeasy', 'speakeasy'),
        ('vegan', 'vegan'),
        ('vegetarian', 'vegetarian'),
        ('view', 'view'),
        ('walkIn', 'walk-in'),
    ]
    vibes = models.JSONField(default=list, blank=True)
    
    # Images (stored as JSON array of URLs)
    images = models.JSONField(default=list, blank=True)
    
    # Legacy fields (keeping for compatibility)
    cuisine = models.CharField(max_length=100, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    price_range = models.CharField(max_length=10, choices=[
        ('$', 'Budget'),
        ('$$', 'Moderate'),
        ('$$$', 'Expensive'),
        ('$$$$', 'Very Expensive'),
    ], default='$$', blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-rating', 'name']
    
    def get_today_hours(self):
        """Get today's operating hours"""
        if not self.operating_hours:
            return None
        
        from datetime import datetime
        today = datetime.now().strftime('%A').lower()
        return self.operating_hours.get(today, None)
    
    def get_vibes_display(self):
        """Get formatted vibes for display"""
        if not self.vibes:
            return []
        
        vibes_dict = dict(self.VIBES_CHOICES)
        return [vibes_dict.get(vibe, vibe) for vibe in self.vibes]
