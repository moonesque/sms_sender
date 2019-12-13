from django.conf import settings
from rest_framework import viewsets, views
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from kavenegar import KavenegarAPI

from .models import Contact, ContactGroup
from .serializers import ContactSerializer, ContactGroupSerializer, SendSMSSerializer


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    lookup_field = 'contact_id'

    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)


class ContactGroupViewSet(viewsets.ModelViewSet):
    serializer_class = ContactGroupSerializer
    lookup_field = 'group_id'

    def get_queryset(self):
        return ContactGroup.objects.filter(owner=self.request.user)


class SendSMSView(views.APIView):
    def post(self, request):
        serializer = SendSMSSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contacts = [c for c in serializer.data['contacts'] if c.startswith('c-')]
        contacts = Contact.objects.filter(owner=request.user, contact_id__in=contacts)
        groups = [g for g in request.data['contacts'] if g.startswith('g-')]
        groups = ContactGroup.objects.filter(owner=request.user, group_id__in=groups)
        all_contacts = list(contacts)
        for g in groups:
            all_contacts.extend(list(g.contacts.all()))
        if not all_contacts:
            raise ValidationError(detail=[{'non_field_error': 'no valid contact found'}])
        sorted_contacts = sorted(all_contacts, key=lambda x: x.contact_id)
        j = sorted_contacts[0]
        targets = [j]
        for i in sorted_contacts[1:]:
            if i.contact_id != j.contact_id:
                j = i
                targets.append(i)
        api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
        for target in targets:
            params = {
                'sender': '1000596446',
                'receptor': str(target.phone),
                'message': serializer.data['message']
            }
            api.sms_send(params)
        return Response()
