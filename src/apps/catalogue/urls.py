from rest_framework import routers
from catalogue import views


router = routers.SimpleRouter()
router.register(r"", views.ProductViewSet)
