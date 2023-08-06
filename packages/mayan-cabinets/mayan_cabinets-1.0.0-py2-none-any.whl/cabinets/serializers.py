from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse

from rest_framework_recursive.fields import RecursiveField

from documents.models import Document
from documents.serializers import DocumentSerializer

from .models import Cabinet


class CabinetSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, read_only=True)
    documents = serializers.HyperlinkedIdentityField(
        view_name='rest_api:cabinet-document-list'
    )
    documents_count = serializers.SerializerMethodField()
    full_path = serializers.SerializerMethodField()

    # This is here because parent is optional in the model but the serializer
    # sets it as required.
    parent = serializers.IntegerField(default=None, required=False)

    class Meta:
        extra_kwargs = {
            'url': {'view_name': 'rest_api:cabinet-detail'},
        }
        fields = (
            'children', 'documents', 'documents_count', 'full_path', 'id',
            'label', 'parent', 'url'
        )
        model = Cabinet

    def get_documents_count(self, obj):
        return obj.get_document_count(user=self.context['request'].user)

    def get_full_path(self, obj):
        return obj.get_full_path()


class NewCabinetSerializer(serializers.ModelSerializer):
    documents = serializers.CharField(
        help_text=_(
            'Comma separated list of document primary keys to add to this '
            'cabinet.'
        ), required=False
    )

    # This is here because parent is optional in the model but the serializer
    # sets it as required.
    parent = serializers.IntegerField(default=None, required=False)

    class Meta:
        fields = ('documents', 'label', 'id', 'parent')
        model = Cabinet

    def create(self, validated_data):
        document_pk_list = validated_data.pop('documents', '')

        result = super(NewCabinetSerializer, self).create(validated_data)

        if document_pk_list:
            try:
                pk_list = document_pk_list.split(',')

                for document in Document.objects.filter(pk__in=pk_list):
                    result.documents.add(document)
            except Exception as exception:
                raise ValidationError(exception)

        return result


class CabinetDocumentSerializer(DocumentSerializer):
    remove = serializers.SerializerMethodField()

    def get_remove(self, instance):
        return reverse(
            'rest_api:cabinet-document', args=(
                self.context['cabinet'].pk, instance.pk
            ), request=self.context['request'], format=self.context['format']
        )

    class Meta(DocumentSerializer.Meta):
        fields = DocumentSerializer.Meta.fields + ('remove',)
        read_only_fields = DocumentSerializer.Meta.fields


class NewCabinetDocumentSerializer(serializers.Serializer):
    documents = serializers.CharField(
        help_text=_(
            'Comma separated list of document primary keys to add to this '
            'cabinet.'
        )
    )

    def create(self, validated_data):
        document_pk_list = validated_data['documents']

        if document_pk_list:
            try:
                pk_list = document_pk_list.split(',')

                for document in Document.objects.filter(pk__in=pk_list):
                    validated_data['cabinet'].documents.add(document)
            except Exception as exception:
                raise ValidationError(exception)

        return {'documents': validated_data['documents']}
