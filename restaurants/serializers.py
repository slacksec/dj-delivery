from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Restaurant, OpenHours, MenuItem

User = get_user_model()
#validate hours

class OpenHoursSerializer(serializers.ModelSerializer):

    day_display = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()
    
    class Meta:
        model = OpenHours
        fields = ('restaurant', 'links', 'day', 'day_display', 'from_hour', 'to_hour')
        
    def get_day_display(self, obj):
        return obj.get_day_display()

    def get_links(self, obj):
        request = self.context['request']
        return {
            'restaurant': reverse(
                'restaurant-detail',
                kwargs={'pk':obj.restaurant.pk,
                        'slug':obj.restaurant.slug},
                request=request
            )
        }

class MenuItemSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = ('restaurant', 'name', 'description', 'price', 
            'availability', 'links')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self' : reverse('menu-item-detail',
                kwargs={'slug':obj.restaurant.slug, 
                        'pk':obj.pk},
                        request=request)
        }

class RestaurantSerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ('name', 'address', 'description', 'cuisine',
            'price', 'delivers', 'site_url', 'links')

    def get_links(self, obj):
        request = self.context['request']
        links = {
            'self': reverse('restaurant-detail',
                kwargs={'slug':obj.slug},request=request),
            'hours': None,
            'menu': None
        }

        if obj.open_hours: 
            links['hours'] = reverse('open-hours',
                kwargs={'slug':obj.slug}, request=request)

        if obj.menu_item:
            links['menu'] = reverse('menu-item-list',
                kwargs={'slug':obj.slug}, request=request)

        return links

        

