import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.constants import CONSUMED
from api.models import Workflow
from api.serializers.workflow_serializers import (WorkflowDetailsSerializer,
                                                  WorkflowRegisterSerializer)
from api.utils.paginator.custom_paginations import Pagination
from api.utils.queue.redis_queue import RedisQueue


class WorkflowConsumeView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        q = RedisQueue('workflows')

        if not q.empty():
            # Dequeueing
            workflow_public_id = q.get().decode('utf-8')

            try:
                workflow = Workflow.objects.get(
                    public_id=workflow_public_id,
                )
            except ObjectDoesNotExist:
                payload = {
                    'status': 'fail',
                    'data': None,
                }
                return Response(payload, status=status.HTTP_404_NOT_FOUND)

            workflow.produced_by = request.user
            workflow.status = CONSUMED
            workflow.save()

            # ToDo: Generate CSV from JSON

            serialized_workflow = WorkflowDetailsSerializer(
                workflow)

            payload = {
                'status': 'success',
                'data': {
                    'workflow': serialized_workflow.data,
                },
            }
            return Response(payload, status=status.HTTP_200_OK)

        payload = {
            'status': 'fail',
            'data': None,
        }
        return Response(payload, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
