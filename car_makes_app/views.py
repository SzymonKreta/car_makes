import requests

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError

from . import models, serializers


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    max_page_size = 100


class PopularPagination(StandardPagination):
    page_size = 5
    max_page_size = 10


class CarViewset(viewsets.ModelViewSet):
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarSerializer
    pagination_class = StandardPagination
    ordering = ['id']
    http_method_names = ['get', 'post', 'head']

    def get_queryset(self):
        cars = list(self.queryset)
        for car in  cars:
            rates = [rate.rate for rate in models.Rate.objects.filter(car=car.id)]
            car.avg = sum(rates)/len(rates) if rates else 0
        return cars

    def perform_create(self, serializer):
        make, model = self.request.POST['make'].lower(), self.request.POST['model'].lower()
        ext_api_response = requests.get(f'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{make}?format=json')
        if not ext_api_response.json()['Count']:
            raise ValidationError('This make does not exists at all')
        if model not in [model['Model_Name'].lower() for model in ext_api_response.json()['Results']]:
            raise ValidationError('This model does not exists at all')
        queryset = models.Car.objects.filter(make=make, model=model)
        if queryset.exists():
            raise ValidationError('Model exists in database')
        serializer.save()


class PopularViewset(viewsets.ModelViewSet):
    queryset = models.Car.objects.all()
    serializer_class = serializers.PopularSerializer
    pagination_class = PopularPagination
    http_method_names = ['get', 'head']

    def get_queryset(self):
        cars = list(self.queryset)
        for car in  self.queryset:
            car.count = len(models.Rate.objects.filter(car=car.id))
        return sorted(cars, key=lambda x: x.count, reverse=True)


class RateViewset(viewsets.ModelViewSet):
    queryset = models.Rate.objects.all()
    serializer_class = serializers.RateSerializer
    ordering = ['id']
    http_method_names = ['post', 'head']
