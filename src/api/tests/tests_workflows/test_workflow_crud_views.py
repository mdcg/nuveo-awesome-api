import hashlib

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.seeds.models import UserFactory, WorkflowFactory
from rest_framework_jwt.settings import api_settings


class WorkflowCRUDAPITestCase(APITestCase):
    def setUp(self):
        self.super_secret_password = hashlib.sha256().hexdigest()
        self.user = UserFactory(password=self.super_secret_password)

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(self.user)

        self.token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        self.workflow = WorkflowFactory()

    def test_workflow_post_create_success(self):
        url = reverse('workflow')
        payload = WorkflowFactory.generate_JSON()

        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.data.get('status'), 'success')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_workflow_post_create_fail_no_credentials_informed(self):
        url = reverse('workflow')
        payload = WorkflowFactory.generate_JSON()

        self.client.credentials(
            HTTP_AUTHORIZATION='')

        response = self.client.get(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_workflow_post_create_fail_malformed_request(self):
        url = reverse('workflow')

        malformed_payload = {
            'data': '',
            'steps': ''
        }

        response = self.client.post(url, malformed_payload, format='json')
        self.assertEqual(response.data.get('status'), 'fail')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_workflow_get_list_success(self):
        url = reverse('workflow')
        WorkflowFactory.create_batch(10)

        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.data.get('status'), 'success')
        # It's 11 because we already created a setUp workflow
        self.assertEqual(response.data.get('data')['count'], 11)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_workflow_get_fail_no_credentials_informed(self):
        url = reverse('workflow')
        self.client.credentials(
            HTTP_AUTHORIZATION='')

        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_workflow_details_patch_update_success(self):
        url = reverse(
            'workflow-details',
            kwargs={
                'workflow_public_id': self.workflow.public_id,
            }
        )
        payload = WorkflowFactory.generate_JSON()

        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.data.get('status'), 'success')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_workflow_details_patch_fail_malformed_request(self):
        url = reverse(
            'workflow-details',
            kwargs={
                'workflow_public_id': self.workflow.public_id,
            }
        )
        malformed_payload = {
            'data': '',
            'steps': ''
        }

        response = self.client.patch(url, malformed_payload, format='json')
        self.assertEqual(response.data.get('status'), 'fail')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_workflow_details_patch_fail_no_credentials_informed(self):
        url = reverse(
            'workflow-details',
            kwargs={
                'workflow_public_id': self.workflow.public_id,
            }
        )
        payload = WorkflowFactory.generate_JSON()

        self.client.credentials(
            HTTP_AUTHORIZATION='')

        response = self.client.get(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_workflow_details_delete_success(self):
        url = reverse(
            'workflow-details',
            kwargs={
                'workflow_public_id': self.workflow.public_id,
            }
        )
        response = self.client.delete(url, {}, format='json')
        self.assertEqual(response.data.get('status'), 'success')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(url, {}, format='json')
        self.assertEqual(response.data.get('status'), 'fail')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_workflow_details_delete_fail_no_credentials_informed(self):
        url = reverse(
            'workflow-details',
            kwargs={
                'workflow_public_id': self.workflow.public_id,
            }
        )
        payload = WorkflowFactory.generate_JSON()

        self.client.credentials(
            HTTP_AUTHORIZATION='')

        response = self.client.delete(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_workflow_details_get_success(self):
        url = reverse(
            'workflow-details',
            kwargs={
                'workflow_public_id': self.workflow.public_id,
            }
        )
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.data.get('status'), 'success')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_workflow_details_get_fail_no_credentials_informed(self):
        url = reverse(
            'workflow-details',
            kwargs={
                'workflow_public_id': self.workflow.public_id,
            }
        )
        self.client.credentials(
            HTTP_AUTHORIZATION='')

        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
