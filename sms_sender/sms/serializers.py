from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .models import Contact, ContactGroup
from django.db import transaction


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        read_only_fields = ['contact_id']
        fields = ['name', 'phone', 'contact_id']

    def create(self, validated_data):
        return Contact.objects.create(**validated_data, owner=self.context['request'].user)


class ContactGroupSerializer(serializers.ModelSerializer):
    contacts = SlugRelatedField(many=True, slug_field='contact_id', queryset=Contact.objects.all())

    class Meta:
        model = ContactGroup
        read_only_fields = ['group_id']
        fields = ['name', 'contacts', 'group_id']

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user
        group = ContactGroup.objects.create(name=validated_data['name'], owner=user)
        contacts = [i.id for i in validated_data['contacts']]
        contacts = Contact.objects.filter(owner=user, id__in=contacts)
        group.contacts.add(*list(contacts))
        return group


class SendSMSSerializer(serializers.Serializer):
    contacts = serializers.ListField(child=serializers.CharField(max_length=18), allow_empty=False)
    message = serializers.CharField()
