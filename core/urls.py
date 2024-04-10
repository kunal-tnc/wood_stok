from django.urls import path

from .views import *

urlpatterns = [
    # Container-related URLs
    path("container/", ContainerListView.as_view(), name="container_list"),
    path("container/create/", CreateContainerView.as_view(), name="create_container"),
    path(
        "container/<int:pk>/update/",
        UpdateContainerView.as_view(),
        name="update_container",
    ),
    path(
        "container/<int:pk>/delete/",
        DeleteContainerView.as_view(),
        name="delete_container",
    ),
    # Log-related URLs
    path("logs/", LogsListView.as_view(), name="log_list"),
    path(
        "container/logs/create/", LogsFormView.as_view(), name="create_container_logs"
    ),
    path("logs/update/", UpdateLogsView.as_view(), name="update_logs"),
    path(
        "container/log/<int:pk>/delete/",
        DeleteLogsView.as_view(),
        name="delete_container_log",
    ),
    path(
        "container/<int:container_id>/logs/",
        ContainerLogsView.as_view(),
        name="container_logs",
    ),
    path("single_logs_form/", SingleLogsView.as_view(), name="single_logs_form"),
    # Finished log-related URLs
    path(
        "finished_logs_info/create/",
        FinishedLogsInfoView.as_view(),
        name="create_finished_logs_info",
    ),
    path("finishedlog/", FinishedLogsView.as_view(), name="finished_log"),
    path("finishedlogs/", FinishedListView.as_view(), name="finishedlogs_list"),
    path(
        "finishedlogs/delete/", DeleteFinishedlogs.as_view(), name="delete_finishedlog"
    ),
    path("finished-logs/", FinishedLogsList.as_view(), name="finished_logs_list"),
    # Authentication and signup URLs
    path("signup/", SignupView.as_view(), name="signup"),
    path("", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
