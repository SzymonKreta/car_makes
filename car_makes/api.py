from rest_framework import routers

from car_makes_app import views as car_makes_views

router = routers.DefaultRouter()
router.register(r'cars', car_makes_views.CarViewset)
router.register(r'rate', car_makes_views.RateViewset)
router.register(r'popular', car_makes_views.PopularViewset)
