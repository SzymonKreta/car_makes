from rest_framework import routers

from car_makes_app import views as car_makes_views

router = routers.DefaultRouter()
router.register(r'cars', car_makes_views.CarViewset, basename='cars')
router.register(r'rate', car_makes_views.RateViewset, basename='rate')
router.register(r'popular', car_makes_views.PopularViewset, basename='popular')
