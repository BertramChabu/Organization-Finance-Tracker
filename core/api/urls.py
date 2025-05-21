from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, PaymentViewSet , TransactionLogViewSet


router = DefaultRouter()
router.register("r'students", StudentViewSet)
router.register("r'payments", PaymentViewSet)
router.register("r'transactions", TransactionLogViewSet)

urlpatterns = router.urls
