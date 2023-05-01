import asyncio
from datetime import datetime as dt

import django_filters.rest_framework
from django.conf import settings
from real_estate.helpers.get_properties_data import get_properties_data_async
from real_estate.serializers import PropertySerializer
from rest_framework import filters, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import PropertyFilter
from .models import Property
from .serializers import PropertySerializer


class PropertyView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend,
    ]
    filterset_class = PropertyFilter
    ordering_fields = ["id", "created_date", "update_date"]

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = PropertySerializer(data=data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class UpdatePropertiesView(APIView):
    def post(self, _):
        """Download and update Properties into DB"""
        result = []
        updated_date = dt.utcnow()
        response_data = asyncio.run(get_properties_data_async())

        for parser in settings.PARSERS:
            source_data = response_data[parser().source]
            result += parser().parse_data(source_data)

        try:
            for data in result:
                source_id = data.pop("source_id")
                data["update_date"] = updated_date
                Property.objects.update_or_create(source_id=source_id, defaults=data)
            return Response(result, status=status.HTTP_200_OK)

        except Exception as err:
            return Response(
                {"error-message": str(err)}, status=status.HTTP_400_BAD_REQUEST
            )
