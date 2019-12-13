from django.urls import path
from rest_framework import routers
from .views import ContactViewSet, ContactGroupViewSet, SendSMSView

router = routers.SimpleRouter()
router.register('contacts', ContactViewSet, base_name='contacts')
router.register('contact_groups', ContactGroupViewSet, base_name='contact_groups')
urlpatterns = router.urls
urlpatterns += [
    path('send_sms/', SendSMSView.as_view())
]
