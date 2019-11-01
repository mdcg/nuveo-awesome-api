from api.models import Workflow
from rest_framework import serializers
from api.serializers.user_serializers import UserDetailsSerializer


class WorkflowRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        exclude = ('created_by', 'updated_by')


class WorkflowDetailsSerializer(serializers.ModelSerializer):
    created_by = UserDetailsSerializer()
    produced_by = UserDetailsSerializer()

    class Meta:
        model = Workflow
        fields = (
            'public_id',
            'status',
            'data',
            'steps',
            'created_by',
            'produced_by,'
        )
