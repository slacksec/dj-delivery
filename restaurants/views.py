from django.shortcuts import render

from rest_framework import (authentication, 
    permissions, viewsets, filters, generics)

from .models import Restaurant, MenuItem, OpenHours
from .serializers import (RestaurantSerializer, MenuItemSerializer,
    OpenHoursSerializer)
from .permissions import HasGroupPermission

class DefaultsMixin(object):
    """Default setings for view authentication, pagination, 
    permissions, and filtering."""

    authentication_classes = (
        authentication.BasicAuthentication,
    )

    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.OrderingFilter
    )

class RestaurantViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing and creating restaurants"""
    #check if a user is a member of restaurant owner group.
    #if not, set permission as read only
    queryset = Restaurant.objects.order_by('name')
    serializer_class = RestaurantSerializer
    lookup_field = ('slug')
    permission_classes = (HasGroupPermission,)
    required_groups = {
        'POST': ['restaurant_owner'],
    }
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class MenuList(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating menu items
    for a specific restaurant
    """
    model = MenuItem
    serializer_class = MenuItemSerializer(many=True)

    def get_queryset(self):
        slug = self.kwargs.get('slug', None)
        if slug is not None:
            restaurant = Restaurant.objects.filter(slug=slug)
            return restaurant.menu_item
        return []

class MenuDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for viewing and editing a menu item instance
    """
    model = MenuItem
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        slug = self.kwargs.get('slug', None)
        if pk is not None and slug is not None:
            menu = Restaurant.objects.filter(slug=slug).menu_item
            item = menu.get(pk=pk)
            return item
        return []

class OpenHoursList(generics.ListCreateAPIView):
    """API endpoint for listing and creating hours for a restaurant"""
    model = OpenHours
    serializer_class = OpenHoursSerializer
    
    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        if pk is not None:
            return OpenHours.objects.filter(restaurant=pk)
        return []
