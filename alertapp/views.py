from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, AlertSerializer
from .models import Alert
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers


class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class CreateAlert(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AlertSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {"message": "Alert created successfully!", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": "Failed to create alert!", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class DeleteAlert(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            alert = Alert.objects.get(pk=pk, user=request.user)
            alert.status = "deleted"
            alert.save()
            return Response(
                {"message": "Alert Deleted!"}, status=status.HTTP_204_NO_CONTENT
            )
        except Alert.DoesNotExist:
            return Response(
                {"detail": "Alert not found!"}, status=status.HTTP_404_NOT_FOUND
            )


class FetchAlerts(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60))
    def get(self, request):
        status_filter = request.query_params.get("status", None)
        alerts = Alert.objects.filter(user=request.user).exclude(status="deleted")
        if status_filter:
            alerts = alerts.filter(status=status_filter)
        alerts = alerts.order_by("-created_at")
        paginator = PageNumberPagination()
        paginator.page_size = 5
        result_page = paginator.paginate_queryset(alerts, request)
        serializer = AlertSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
