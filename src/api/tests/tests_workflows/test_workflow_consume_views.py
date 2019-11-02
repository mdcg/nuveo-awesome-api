import hashlib

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.seeds.models import UserFactory, WorkflowFactory
from api.utils.queue.redis_queue import RedisQueue
from rest_framework_jwt.settings import api_settings


class WorkflowConsumeAPITestCase(APITestCase):
    def setUp(self):
        self.super_secret_password = hashlib.sha256().hexdigest()
        self.user = UserFactory(password=self.super_secret_password)

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(self.user)

        self.token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        self.q = RedisQueue('workflows')

    def test_workflow_post_consume_success(self):
        self.q.flush()
        url = reverse('workflow')
        payload = WorkflowFactory.generate_JSON()

        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.data.get('status'), 'success')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('workflow-consume')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_workflow_post_consume_fail_no_credentials_informed(self):
        url = reverse('workflow-consume')
        self.client.credentials(
            HTTP_AUTHORIZATION='')

        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_workflow_post_consume_fail_no_workflow_to_consume(self):
        self.q.flush()
        url = reverse('workflow-consume')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)