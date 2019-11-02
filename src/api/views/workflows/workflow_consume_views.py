import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
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
from api.utils.converter.json_to_csv import export_json_to_csv
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
            # http://codingpole.com/blog/using-django-rest-framework-for-csv-export/
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="workflow-{workflow_public_id}.csv"'

            return export_json_to_csv(json_data=workflow.data, response=response)

        payload = {
            'status': 'fail',
            'data': None,
        }
        return Response(payload, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
