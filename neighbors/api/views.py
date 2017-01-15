from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import detail_route
from rest_framework.pagination import LimitOffsetPagination

from neighbors.core.models import User
from neighbors.api.serializers import UserSerializer, NearestNeighborsQueryParams


class CustomLimitOffsetPagination(LimitOffsetPagination):

    max_limit = 100
    default_limit = 10


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomLimitOffsetPagination

    @detail_route()
    def nearest_neighbors(self, request, pk):
        query_params = request.query_params
        errors = self.validate_query_params(query_params)
        if errors:
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

        neighbors = self.get_object().get_nearest_users(
            float(query_params['radius']), int(query_params['limit']))
        return Response(data=UserSerializer(neighbors, many=True).data)

    @staticmethod
    def validate_query_params(query_params):
        serializer = NearestNeighborsQueryParams(data=query_params)
        if not serializer.is_valid():
            return serializer.errors
