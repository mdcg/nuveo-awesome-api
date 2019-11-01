from django.urls import path

from api.views.users.user_authentication_views import SignInView, SignUpView
from api.views.workflows.workflow_crud_views import WorkflowView, WorkflowDetailsView
from api.views.workflows.workflow_consume_views import WorkflowConsumeView

urlpatterns = [
    path('signin', SignInView.as_view(), name='signin'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('workflow', WorkflowView.as_view(), name='workflow'),
    path('workflow/consume', WorkflowConsumeView.as_view(), name='workflow-consume'),
    path('workflow/<uuid:workflow_public_id>', WorkflowDetailsView.as_view(), name='workflow-details'),
]