from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from bson import ObjectId
from .mongodb import MongoDBClient
from .serializers import RoadmapSerializer

client = MongoDBClient()


class ListDatabases(APIView):
    def get(self, request):
        databases = client.list_databases()
        return Response(databases)


class ListCollections(APIView):
    def get(self, request):
        collections = client.list_collections()
        return Response(collections)


class ListDocuments(APIView):
    def get(self, request, collection_name):
        filters = request.query_params.dict()
        documents = client.list_documents(collection_name, filters)
        for doc in documents:
            doc['_id'] = str(doc['_id'])
        return Response(documents)


class DocumentDetail(APIView):
    def get(self, request, collection_name, document_id):
        document = client.list_documents(collection_name, {'_id': ObjectId(document_id)})
        if document:
            document[0]['_id'] = str(document[0]['_id'])
            return Response(document[0])
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, collection_name, document_id):
        serializer = RoadmapSerializer(data=request.data)
        if serializer.is_valid():
            filter = {'_id': ObjectId(document_id)}
            update = serializer.validated_data
            matched, modified = client.update_document(collection_name, filter, update)
            return Response({'matched': matched, 'modified': modified})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, collection_name, document_id):
        filter = {'_id': ObjectId(document_id)}
        deleted_count = client.delete_document(collection_name, filter)
        return Response({'deleted_count': deleted_count})


class AddDocument(generics.CreateAPIView):
    serializer_class = RoadmapSerializer

    def perform_create(self, serializer):
        collection_name = self.kwargs['collection_name']
        client.add_document(collection_name, serializer.validated_data)


class AddDocuments(APIView):
    def post(self, request, collection_name):
        serializer = RoadmapSerializer(data=request.data, many=True)
        if serializer.is_valid():
            inserted_ids = client.add_documents(collection_name, serializer.validated_data)
            return Response({'inserted_ids': inserted_ids}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
