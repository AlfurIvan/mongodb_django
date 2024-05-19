
from django.urls import path
from .views import (
    ListDatabases, ListCollections, ListDocuments, DocumentDetail, AddDocument, AddDocuments
)

urlpatterns = [
    path('databases/', ListDatabases.as_view(), name='list-databases'),
    path('databases/collections/', ListCollections.as_view(), name='list-collections'),
    path('databases/collections/<str:collection_name>/documents/', ListDocuments.as_view(), name='list-documents'),
    path('databases/collections/<str:collection_name>/documents/<str:document_id>/', DocumentDetail.as_view(), name='document-detail'),
    path('databases/collections/<str:collection_name>/documents/add/', AddDocument.as_view(), name='add-document'),
    path('databases/collections/<str:collection_name>/documents/add-many/', AddDocuments.as_view(), name='add-documents'),
]