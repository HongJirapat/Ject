from django.urls import path
from thread.views import *

urlpatterns = [
    path("", ThreadListView.as_view(), name="thread-list"),
    path("<int:pk>", ThreadDetailView.as_view(), name="thread-detail"),
    path("create", ThreadCreateView.as_view(), name="thread-create"),
    path("create/create-category", CreateCategoryView.as_view(), name="create-category"),
    path('history/', ThreadHistoryView.as_view(), name='thread-history'),
    path("edit/<int:pk>", ThreadEditView.as_view(), name="thread-edit"),
    path("delete/<int:pk>", ThreadDeleteView.as_view(), name="thread-delete"),
]