from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import override_settings

from rest_framework.test import APITestCase

from documents.models import DocumentType
from documents.tests import TEST_DOCUMENT_TYPE
from user_management.tests.literals import (
    TEST_ADMIN_EMAIL, TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME
)

from ..models import Cabinet

from .literals import (
    TEST_CABINET_EDITED_LABEL, TEST_CABINET_LABEL, TEST_SMALL_DOCUMENT_PATH
)


@override_settings(OCR_AUTO_OCR=False)
class CabinetAPITestCase(APITestCase):
    """
    Test the cabinet API endpoints
    """

    def setUp(self):
        super(CabinetAPITestCase, self).setUp()

        self.admin_user = get_user_model().objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )

        self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )

        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=file_object,
            )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document_2 = self.document_type.new_document(
                file_object=file_object,
            )

    def tearDown(self):
        self.document_type.delete()
        super(CabinetAPITestCase, self).tearDown()

    def test_cabinet_create(self):
        response = self.client.post(
            reverse('rest_api:cabinet-list'), {'label': TEST_CABINET_LABEL}
        )

        cabinet = Cabinet.objects.first()

        self.assertEqual(response.data['id'], cabinet.pk)
        self.assertEqual(response.data['label'], TEST_CABINET_LABEL)

        self.assertEqual(Cabinet.objects.count(), 1)
        self.assertEqual(cabinet.label, TEST_CABINET_LABEL)

    def test_cabinet_create_with_single_document(self):
        response = self.client.post(
            reverse('rest_api:cabinet-list'), {
                'label': TEST_CABINET_LABEL, 'documents': '{}'.format(
                    self.document.pk
                )
            }
        )

        cabinet = Cabinet.objects.first()

        self.assertEqual(response.data['id'], cabinet.pk)
        self.assertEqual(response.data['label'], TEST_CABINET_LABEL)

        self.assertQuerysetEqual(
            cabinet.documents.all(), (repr(self.document),)
        )
        self.assertEqual(cabinet.label, TEST_CABINET_LABEL)

    def test_cabinet_create_with_multiple_documents(self):
        response = self.client.post(
            reverse('rest_api:cabinet-list'), {
                'label': TEST_CABINET_LABEL, 'documents': '{},{}'.format(
                    self.document.pk, self.document_2.pk
                )
            }
        )

        cabinet = Cabinet.objects.first()

        self.assertEqual(response.data['id'], cabinet.pk)
        self.assertEqual(response.data['label'], TEST_CABINET_LABEL)

        self.assertEqual(Cabinet.objects.count(), 1)

        self.assertEqual(cabinet.label, TEST_CABINET_LABEL)

        self.assertQuerysetEqual(
            cabinet.documents.all(), map(
                repr, (self.document, self.document_2)
            )
        )

    def test_cabinet_delete(self):
        cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)

        self.client.delete(
            reverse('rest_api:cabinet-detail', args=(cabinet.pk,))
        )

        self.assertEqual(Cabinet.objects.count(), 0)

    def test_cabinet_edit(self):
        cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)

        self.client.put(
            reverse('rest_api:cabinet-detail', args=(cabinet.pk,)),
            {'label': TEST_CABINET_EDITED_LABEL}
        )

        cabinet.refresh_from_db()

        self.assertEqual(cabinet.label, TEST_CABINET_EDITED_LABEL)

    def test_cabinet_add_document(self):
        cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)

        self.client.post(
            reverse('rest_api:cabinet-document-list', args=(cabinet.pk,)), {
                'documents': '{}'.format(self.document.pk)
            }
        )

        self.assertQuerysetEqual(
            cabinet.documents.all(), (repr(self.document),)
        )

    def test_cabinet_add_multiple_documents(self):
        cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)

        self.client.post(
            reverse('rest_api:cabinet-document-list', args=(cabinet.pk,)), {
                'documents': '{},{}'.format(
                    self.document.pk, self.document_2.pk
                )
            }
        )

        self.assertQuerysetEqual(
            cabinet.documents.all(), map(
                repr, (self.document, self.document_2)
            )
        )

    def test_cabinet_remove_document(self):
        cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)

        cabinet.documents.add(self.document)

        self.client.delete(
            reverse(
                'rest_api:cabinet-document', args=(
                    cabinet.pk, self.document.pk
                )
            ),
        )

        self.assertEqual(cabinet.documents.count(), 0)
