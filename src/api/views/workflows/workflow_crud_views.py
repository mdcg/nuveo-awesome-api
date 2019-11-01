from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Workflow
from api.serializers.workflow_serializers import (WorkflowDetailsSerializer,
                                                  WorkflowRegisterSerializer)
from api.utils.paginator.custom_paginations import Pagination
from api.utils.queue.redis_queue import RedisQueue


class WorkflowView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        workflow_informed_data = WorkflowRegisterSerializer(
            data=request.data)

        if workflow_informed_data.is_valid():
            workflow = workflow_informed_data.save(created_by=request.user)

            serialized_workflow = WorkflowDetailsSerializer(
                workflow)

            # Queuing
            q = RedisQueue('workflows')
            q.put(str(workflow.public_id))

            payload = {
                'status': 'success',
                'data': {
                    'workflow': serialized_workflow.data,
                },
            }
            return Response(payload, status=status.HTTP_201_CREATED)

        payload = {
            'status': 'fail',
            'data': {
                **workflow_informed_data.errors,
            },
        }
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        workflows = Workflow.objects.all()

        paginator = Pagination()
        result_page = paginator.paginate_queryset(
            workflows, request)

        serialized_workflows = WorkflowDetailsSerializer(
            result_page, many=True)

        payload = {
            'status': 'success',
            'data': paginator.get_paginated_response({
                'workflow': serialized_workflows.data,
            }),
        }
        return Response(payload, status=status.HTTP_200_OK)


class WorkflowDetailsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, workflow_public_id):
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

        serialized_workflow = WorkflowDetailsSerializer(
            workflow)

        payload = {
            'status': 'success',
            'data': {
                'workflow': serialized_workflow.data,
            },
        }
        return Response(payload, status=status.HTTP_200_OK)

    def patch(self, request, workflow_public_id):
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

        workflow_informed_data_to_update = WorkflowRegisterSerializer(
            workflow, data=request.data, partial=True)

        if workflow_informed_data_to_update.is_valid():
            workflow = workflow_informed_data_to_update.save()

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
            'data': {
                **workflow_informed_data_to_update.errors,
            },
        }
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, workflow_public_id):
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

        serialized_workflow = WorkflowDetailsSerializer(
            workflow)

        workflow.delete()

        payload = {
            'status': 'success',
            'data': {
                'workflow': serialized_workflow.data,
            },
        }
        return Response(payload, status=status.HTTP_200_OK)
