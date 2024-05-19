import json
from rest_framework import status
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

    def get_filters(self, request):
        try:
            filters_str = request.query_params.dict()["filter"]
            filters = json.loads(filters_str)
        except KeyError:
            filters = {}
        return filters

    def get(self, request, collection_name):
        filters = self.get_filters(request)
        documents = client.list_documents(collection_name, filters)
        for doc in documents:
            doc['_id'] = str(doc['_id'])
        return Response(documents)

    def put(self, request, collection_name):
        filters = self.get_filters(request)
        serializer = RoadmapSerializer(data=request.data)
        if serializer.is_valid():
            update = serializer.validated_data
            matched, modified = client.update_documents(collection_name, filters, update)
            return Response({'matched': matched, 'modified': modified})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, collection_name):
        filters = self.get_filters(request)

        if not filters:
            return Response({"message": "I dont want to set the world on fire"})
        deleted_count = client.delete_documents(collection_name, filters)
        return Response({'deleted_count': deleted_count})


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


class CreateDocument(APIView):

    def get(self, request, *args, **kwargs):
        return Response(data={"message": "debug"})

    def post(self, request, collection_name):
        if isinstance(request.data, list):  # Перевіряємо, чи надійшов список документів
            serializer = RoadmapSerializer(data=request.data, many=True)
        else:
            serializer = RoadmapSerializer(data=request.data)

        if serializer.is_valid():
            if isinstance(request.data, list):  # Якщо надійшов список документів
                inserted_ids = client.add_documents(collection_name, serializer.validated_data)
            else:
                inserted_ids = [client.add_document(collection_name, serializer.validated_data)]

            return Response({'inserted_ids': inserted_ids}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
