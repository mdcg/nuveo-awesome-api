from django.urls import path

from api.views.users.user_authentication_views import SignInView, SignUpView
from api.views.workflows.workflow_crud_views import WorkflowView, WorkflowDetailsView

urlpatterns = [
    path('signin', SignInView.as_view(), name='signin'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('workflow', WorkflowView.as_view(), name='workflow'),
    path('workflow/<uuid:workflow_public_id>', WorkflowDetailsView.as_view(), name='workflow-details'),
]