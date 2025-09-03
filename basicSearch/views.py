from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.cache import cache
from django.conf import settings
from .models import Restaurant


def index(request):
    """Main search page view"""
    return render(request, 'basicSearch/index.html')

def restaurant_detail(request, restaurant_id):
    """Detailed view for a specific restaurant"""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    return render(request, 'basicSearch/restaurant_detail.html', {'restaurant': restaurant})

@csrf_exempt
def search_restaurants(request):
    """AJAX API endpoint for restaurant search with caching"""
    if request.method == 'GET':
        query = request.GET.get('q', '')
        
        # Generate cache key for this search query
        cache_key = f"{settings.CACHE_KEY_PREFIX}:{query.lower().strip()}"
        
        # Try to get cached results first
        cached_results = cache.get(cache_key)
        if cached_results is not None:
            return JsonResponse({
                'success': True,
                'results': cached_results['results'],
                'count': cached_results['count'],
                'cached': True
            })
        
        # Start with all restaurants
        restaurants = Restaurant.objects.all()
        
        # Apply search filter if query provided
        if query:
            restaurants = restaurants.filter(
                Q(name__icontains=query) |
                Q(cuisine__icontains=query) |
                Q(address__icontains=query) |
                Q(neighbourhood__icontains=query)
                # Removed vibes search as it's not supported by SQLite
            )
        
        # Convert to JSON-serializable format for search results
        results = []
        for restaurant in restaurants:
            results.append({
                'id': str(restaurant.id),
                'name': restaurant.name,
                'cuisine': restaurant.cuisine or '',
                'address': restaurant.address,
                'neighbourhood': restaurant.neighbourhood or '',
                'rating': float(restaurant.rating) if restaurant.rating else 0.0,
                'price_range': restaurant.price_range or '',
                'vibes': [vibe.lower() for vibe in restaurant.get_vibes_display()[:3]],  # Show first 3 vibes in lowercase
                'reservation_partner': restaurant.reservation_partner,
                'main_image': restaurant.images[0] if restaurant.images else None,
            })
        
        # Cache the results for 5 minutes
        cache_data = {
            'results': results,
            'count': len(results)
        }
        cache.set(cache_key, cache_data, timeout=300)  # 5 minutes cache
        
        return JsonResponse({
            'success': True,
            'results': results,
            'count': len(results),
            'cached': False
        })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def clear_search_cache(request):
    """Clear all search cache entries"""
    try:
        # Get all cache keys that start with our prefix
        cache_keys = []
        for key in cache._cache.keys():
            if key.startswith(settings.CACHE_KEY_PREFIX):
                cache_keys.append(key)
        
        # Clear all search-related cache entries
        cache.delete_many(cache_keys)
        
        return JsonResponse({
            'success': True,
            'message': f'Cleared {len(cache_keys)} cache entries',
            'cleared_keys': cache_keys
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Failed to clear cache: {str(e)}'
        })

def get_cache_stats(request):
    """Get cache statistics"""
    try:
        # Get cache info (this is a simple implementation)
        cache_info = {
            'backend': 'LocMemCache',
            'timeout': 300,
            'max_entries': 1000,
            'current_entries': len(cache._cache) if hasattr(cache, '_cache') else 'Unknown'
        }
        
        return JsonResponse({
            'success': True,
            'cache_info': cache_info
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Failed to get cache stats: {str(e)}'
        })

def populate_sample_data(request):
    """View to populate sample restaurant data for testing"""
    if Restaurant.objects.count() == 0:
        sample_restaurants = [
            {
                'name': 'Pizza Palace',
                'place_id': 'ChIJN1t_tDeuEmsRUsoyG83frY4',
                'address': '123 Main St, Downtown, City',
                'neighbourhood': 'Downtown',
                'latitude': 40.7128,
                'longitude': -74.0060,
                'cuisine': 'Italian',
                'rating': 4.5,
                'price_range': '$$',
                'phone': '555-0101',
                'website': 'https://pizzapalace.com',
                'reservation_url': 'https://pizzapalace.com/reserve',
                'menu_url': 'https://pizzapalace.com/menu',
                'instagram_url': 'https://instagram.com/pizzapalace',
                'facebook_url': 'https://facebook.com/pizzapalace',
                'x_url': 'https://twitter.com/pizzapalace',
                'tiktok_url': 'https://tiktok.com/@pizzapalace',
                'reservation_partner': 'OpenTable',
                'operating_hours': {
                    'monday': '11:00 AM - 10:00 PM',
                    'tuesday': '11:00 AM - 10:00 PM',
                    'wednesday': '11:00 AM - 10:00 PM',
                    'thursday': '11:00 AM - 10:00 PM',
                    'friday': '11:00 AM - 11:00 PM',
                    'saturday': '11:00 AM - 11:00 PM',
                    'sunday': '12:00 PM - 9:00 PM'
                },
                'vibes': ['casual', 'family-friendly', 'lively'],
                'images': [
                    'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800',
                    'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800',
                    'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=800',
                    'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800',
                    'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=800',
                    'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800',
                    'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800',
                    'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=800',
                    'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800',
                    'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800'
                ]
            },
            {
                'name': 'Sushi Express',
                'place_id': 'ChIJN1t_tDeuEmsRUsoyG83frY5',
                'address': '456 Oak Ave, Midtown, City',
                'neighbourhood': 'Midtown',
                'latitude': 40.7589,
                'longitude': -73.9851,
                'cuisine': 'Japanese',
                'rating': 4.2,
                'price_range': '$$$',
                'phone': '555-0102',
                'website': 'https://sushiexpress.com',
                'reservation_url': 'https://sushiexpress.com/book',
                'menu_url': 'https://sushiexpress.com/menu',
                'instagram_url': 'https://instagram.com/sushiexpress',
                'facebook_url': 'https://facebook.com/sushiexpress',
                'x_url': 'https://twitter.com/sushiexpress',
                'tiktok_url': '',
                'reservation_partner': 'SevenRooms',
                'operating_hours': {
                    'monday': '11:30 AM - 10:30 PM',
                    'tuesday': '11:30 AM - 10:30 PM',
                    'wednesday': '11:30 AM - 10:30 PM',
                    'thursday': '11:30 AM - 10:30 PM',
                    'friday': '11:30 AM - 11:30 PM',
                    'saturday': '11:30 AM - 11:30 PM',
                    'sunday': '12:00 PM - 9:30 PM'
                },
                'vibes': ['upscale', 'trendy', 'romantic'],
                'images': [
                    'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800',
                    'https://images.unsplash.com/photo-1553621042-f6e147245754?w=800',
                    'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800',
                    'https://images.unsplash.com/photo-1553621042-f6e147245754?w=800',
                    'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800',
                    'https://images.unsplash.com/photo-1553621042-f6e147245754?w=800',
                    'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800',
                    'https://images.unsplash.com/photo-1553621042-f6e147245754?w=800',
                    'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800',
                    'https://images.unsplash.com/photo-1553621042-f6e147245754?w=800'
                ]
            },
            {
                'name': 'Steak House',
                'place_id': 'ChIJN1t_tDeuEmsRUsoyG83frY6',
                'address': '654 Maple Dr, Luxury District, City',
                'neighbourhood': 'Luxury District',
                'latitude': 40.7505,
                'longitude': -73.9934,
                'cuisine': 'American',
                'rating': 4.9,
                'price_range': '$$$$',
                'phone': '555-0105',
                'website': 'https://steakhouse.com',
                'reservation_url': 'https://steakhouse.com/reservations',
                'menu_url': 'https://steakhouse.com/menu',
                'instagram_url': 'https://instagram.com/steakhouse',
                'facebook_url': 'https://facebook.com/steakhouse',
                'x_url': 'https://twitter.com/steakhouse',
                'tiktok_url': '',
                'reservation_partner': 'Tock',
                'operating_hours': {
                    'monday': '5:00 PM - 11:00 PM',
                    'tuesday': '5:00 PM - 11:00 PM',
                    'wednesday': '5:00 PM - 11:00 PM',
                    'thursday': '5:00 PM - 11:00 PM',
                    'friday': '5:00 PM - 12:00 AM',
                    'saturday': '5:00 PM - 12:00 AM',
                    'sunday': '5:00 PM - 10:00 PM'
                },
                'vibes': ['luxury', 'elegant', 'romantic', 'upscale'],
                'images': [
                    'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800',
                    'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800',
                    'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800',
                    'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800',
                    'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800',
                    'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800',
                    'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800',
                    'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800',
                    'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800',
                    'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800'
                ]
            },
            {
                'name': 'Amber Garden',
                'place_id': 'ChIJN1t_tDeuEmsRUsoyG83frY7',
                'address': '789 Garden Lane, Riverside, City',
                'neighbourhood': 'Riverside',
                'latitude': 40.7200,
                'longitude': -73.9900,
                'cuisine': 'Asian Fusion',
                'rating': 4.6,
                'price_range': '$$$',
                'phone': '555-0106',
                'website': 'https://ambergarden.com',
                'reservation_url': 'https://ambergarden.com/book',
                'menu_url': 'https://ambergarden.com/menu',
                'instagram_url': 'https://instagram.com/ambergarden',
                'facebook_url': 'https://facebook.com/ambergarden',
                'x_url': 'https://twitter.com/ambergarden',
                'tiktok_url': 'https://tiktok.com/@ambergarden',
                'reservation_partner': 'OpenTable',
                'operating_hours': {
                    'monday': '11:00 AM - 10:00 PM',
                    'tuesday': '11:00 AM - 10:00 PM',
                    'wednesday': '11:00 AM - 10:00 PM',
                    'thursday': '11:00 AM - 10:00 PM',
                    'friday': '11:00 AM - 11:00 PM',
                    'saturday': '11:00 AM - 11:00 PM',
                    'sunday': '12:00 PM - 9:00 PM'
                },
                'vibes': ['aesthetic', 'chic', 'intimate', 'smallplates'],
                'images': [
                    'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800',
                    'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800',
                    'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800',
                    'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800',
                    'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800',
                    'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800',
                    'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800',
                    'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800',
                    'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800',
                    'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800'
                ]
            },
            {
                'name': 'Blue Ocean Seafood',
                'place_id': 'ChIJN1t_tDeuEmsRUsoyG83frY8',
                'address': '321 Harbor View, Waterfront, City',
                'neighbourhood': 'Waterfront',
                'latitude': 40.7100,
                'longitude': -73.9800,
                'cuisine': 'Seafood',
                'rating': 4.4,
                'price_range': '$$$',
                'phone': '555-0107',
                'website': 'https://blueocean.com',
                'reservation_url': 'https://blueocean.com/reserve',
                'menu_url': 'https://blueocean.com/menu',
                'instagram_url': 'https://instagram.com/blueocean',
                'facebook_url': 'https://facebook.com/blueocean',
                'x_url': 'https://twitter.com/blueocean',
                'tiktok_url': 'https://tiktok.com/@blueocean',
                'reservation_partner': 'SevenRooms',
                'operating_hours': {
                    'monday': '5:00 PM - 10:00 PM',
                    'tuesday': '5:00 PM - 10:00 PM',
                    'wednesday': '5:00 PM - 10:00 PM',
                    'thursday': '5:00 PM - 10:00 PM',
                    'friday': '5:00 PM - 11:00 PM',
                    'saturday': '5:00 PM - 11:00 PM',
                    'sunday': '5:00 PM - 9:00 PM'
                },
                'vibes': ['view', 'romantic', 'finedining', 'fresh'],
                'images': [
                    'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800',
                    'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800',
                    'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800',
                    'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800',
                    'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800',
                    'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800',
                    'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800',
                    'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800',
                    'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800',
                    'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800'
                ]
            },
            {
                'name': 'Café Luna',
                'place_id': 'ChIJN1t_tDeuEmsRUsoyG83frY9',
                'address': '567 Moon Street, Arts District, City',
                'neighbourhood': 'Arts District',
                'latitude': 40.7300,
                'longitude': -73.9700,
                'cuisine': 'French Bistro',
                'rating': 4.7,
                'price_range': '$$',
                'phone': '555-0108',
                'website': 'https://cafeluna.com',
                'reservation_url': 'https://cafeluna.com/book',
                'menu_url': 'https://cafeluna.com/menu',
                'instagram_url': 'https://instagram.com/cafeluna',
                'facebook_url': 'https://facebook.com/cafeluna',
                'x_url': 'https://twitter.com/cafeluna',
                'tiktok_url': 'https://tiktok.com/@cafeluna',
                'reservation_partner': 'OpenTable',
                'operating_hours': {
                    'monday': '8:00 AM - 10:00 PM',
                    'tuesday': '8:00 AM - 10:00 PM',
                    'wednesday': '8:00 AM - 10:00 PM',
                    'thursday': '8:00 AM - 10:00 PM',
                    'friday': '8:00 AM - 11:00 PM',
                    'saturday': '9:00 AM - 11:00 PM',
                    'sunday': '9:00 AM - 9:00 PM'
                },
                'vibes': ['cozy', 'romantic', 'brunch', 'aesthetic'],
                'images': [
                    'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800',
                    'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800',
                    'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800',
                    'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800',
                    'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800',
                    'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800',
                    'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800',
                    'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800',
                    'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800',
                    'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800'
                ]
            },
            {
                'name': 'Quattro Stagioni',
                'place_id': 'ChIJN1t_tDeuEmsRUsoyG83frY10',
                'address': '890 Seasons Blvd, Historic Quarter, City',
                'neighbourhood': 'Historic Quarter',
                'latitude': 40.7400,
                'longitude': -73.9600,
                'cuisine': 'Italian Fine Dining',
                'rating': 4.8,
                'price_range': '$$$$',
                'phone': '555-0109',
                'website': 'https://quattrostagioni.com',
                'reservation_url': 'https://quattrostagioni.com/reserve',
                'menu_url': 'https://quattrostagioni.com/menu',
                'instagram_url': 'https://instagram.com/quattrostagioni',
                'facebook_url': 'https://facebook.com/quattrostagioni',
                'x_url': 'https://twitter.com/quattrostagioni',
                'tiktok_url': 'https://tiktok.com/@quattrostagioni',
                'reservation_partner': 'Tock',
                'operating_hours': {
                    'monday': '6:00 PM - 11:00 PM',
                    'tuesday': '6:00 PM - 11:00 PM',
                    'wednesday': '6:00 PM - 11:00 PM',
                    'thursday': '6:00 PM - 11:00 PM',
                    'friday': '6:00 PM - 12:00 AM',
                    'saturday': '6:00 PM - 12:00 AM',
                    'sunday': '6:00 PM - 10:00 PM'
                },
                'vibes': ['luxury', 'elegant', 'finedining', 'michelin', 'romantic'],
                'images': [
                    'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800',
                    'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800',
                    'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800',
                    'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800',
                    'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800',
                    'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800',
                    'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800',
                    'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800',
                    'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800',
                    'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800'
                ]
            },
            {
                'name': 'Bella Vista',
                'place_id': 'ChIJN1t_tDeuEmsRUsoyG83frY11',
                'address': '456 Hilltop Road, Mountain View, City',
                'neighbourhood': 'Mountain View',
                'latitude': 40.7500,
                'longitude': -73.9500,
                'cuisine': 'Mediterranean',
                'rating': 4.3,
                'price_range': '$$',
                'phone': '555-0110',
                'website': 'https://bellavista.com',
                'reservation_url': 'https://bellavista.com/book',
                'menu_url': 'https://bellavista.com/menu',
                'instagram_url': 'https://instagram.com/bellavista',
                'facebook_url': 'https://facebook.com/bellavista',
                'x_url': 'https://twitter.com/bellavista',
                'tiktok_url': 'https://tiktok.com/@bellavista',
                'reservation_partner': 'OpenTable',
                'operating_hours': {
                    'monday': '12:00 PM - 10:00 PM',
                    'tuesday': '12:00 PM - 10:00 PM',
                    'wednesday': '12:00 PM - 10:00 PM',
                    'thursday': '12:00 PM - 10:00 PM',
                    'friday': '12:00 PM - 11:00 PM',
                    'saturday': '12:00 PM - 11:00 PM',
                    'sunday': '1:00 PM - 9:00 PM'
                },
                'vibes': ['view', 'patio', 'family-friendly', 'casual'],
                'images': [
                    'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800',
                    'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800',
                    'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800',
                    'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800',
                    'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800',
                    'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800',
                    'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800',
                    'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800',
                    'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800',
                    'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800'
                ]
            },
            {
                'name': 'Crystal Palace',
                'place_id': 'ChIJN1t_tDeuEmsRUsoyG83frY12',
                'address': '789 Crystal Avenue, Luxury District, City',
                'neighbourhood': 'Luxury District',
                'latitude': 40.7600,
                'longitude': -73.9400,
                'cuisine': 'International',
                'rating': 4.9,
                'price_range': '$$$$',
                'phone': '555-0111',
                'website': 'https://crystalpalace.com',
                'reservation_url': 'https://crystalpalace.com/reserve',
                'menu_url': 'https://crystalpalace.com/menu',
                'instagram_url': 'https://instagram.com/crystalpalace',
                'facebook_url': 'https://facebook.com/crystalpalace',
                'x_url': 'https://twitter.com/crystalpalace',
                'tiktok_url': 'https://tiktok.com/@crystalpalace',
                'reservation_partner': 'Tock',
                'operating_hours': {
                    'monday': '6:00 PM - 11:00 PM',
                    'tuesday': '6:00 PM - 11:00 PM',
                    'wednesday': '6:00 PM - 11:00 PM',
                    'thursday': '6:00 PM - 11:00 PM',
                    'friday': '6:00 PM - 12:00 AM',
                    'saturday': '6:00 PM - 12:00 AM',
                    'sunday': '6:00 PM - 10:00 PM'
                },
                'vibes': ['luxury', 'elegant', 'finedining', 'michelin', 'privatedining'],
                'images': [
                    'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800',
                    'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800',
                    'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800',
                    'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800',
                    'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800',
                    'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800',
                    'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800',
                    'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800',
                    'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800',
                    'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800'
                ]
            }
        ]
        
        for data in sample_restaurants:
            Restaurant.objects.create(**data)
        
        return HttpResponse("Sample data populated successfully!")
    
    return HttpResponse("Sample data already exists!")