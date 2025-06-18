from django.urls import path, include
from rest_framework.routers import DefaultRouter

from objects.views import (
    BuildingViewSet,
    ComplaintViewSet,
    # ComplaintMicroServiceViewSet,
    DocumentKeyFileViewSet,
    BuildingHistoryViewSet,
    SmsGetBalanceViewSet,
    BuildingCoordinateViewSet,
    EvacAddressViewSet,
    FAQViewSet,
    SubBuildingViewSet,
    DocumentKeyViewSet
)

router = DefaultRouter()
router.register('doc-keys', DocumentKeyViewSet, basename='doc-keys')
router.register('buildings', BuildingViewSet, basename='buildings')
router.register('complaint', ComplaintViewSet, basename='complaint')
router.register('document', DocumentKeyFileViewSet, basename='building_document_keys')
router.register('buildings', BuildingHistoryViewSet, basename='building_document_history')
router.register('building/coordinates', BuildingCoordinateViewSet, basename='building_coordinate')
router.register(
    r'buildings/(?P<building_id>\d+)/subbuildings',
    SubBuildingViewSet, basename='subbuildings'
)
router.register('evac/address', EvacAddressViewSet, basename='evac_address')
# router.register('faq', FAQViewSet, basename='faq')

urlpatterns = [
    path('', include(router.urls)),
    path('get/balance', SmsGetBalanceViewSet.as_view()),
    # path('microservice/complaint/<int:pk>/mark_as_answered/',
    #          ComplaintMicroServiceViewSet.as_view({'post': 'mark_as_answered'}),
    #          name='complaint-mark-as-answered'),
]
