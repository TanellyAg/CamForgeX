import uuid
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from .models import Track
from .serializers import (
    TrackSerializer,
    ProcessTrackRequestSerializer,
    TrackProcessingStatusSerializer,
    JobSerializer,  # NEW
)

class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

    @extend_schema(
        tags=["Tracks", "AI Processing"],
        summary="Start AI processing for a track (denoise, add beats)",
        request=ProcessTrackRequestSerializer,
        responses={202: TrackProcessingStatusSerializer},
    )
    @action(detail=True, methods=["post"], url_path="process")
    def process(self, request, pk=None):
        payload = ProcessTrackRequestSerializer(data=request.data)
        payload.is_valid(raise_exception=True)
        job_id = str(uuid.uuid4())
        return Response({"job_id": job_id, "status": "queued"}, status=status.HTTP_202_ACCEPTED)

# Make this a GenericViewSet so drf-spectacular can infer basics from serializer_class
class JobViewSet(viewsets.GenericViewSet):
    serializer_class = JobSerializer
    lookup_field = "id"        # make the path param explicit and named "id"
    lookup_url_kwarg = "id"

    @extend_schema(
        tags=["AI Jobs"],
        summary="List processing jobs",
        responses=JobSerializer(many=True),
    )
    def list(self, request):
        # Stubbed example
        data = [{"id": "sample-job-1", "status": "queued"}]
        return Response(data)

    @extend_schema(
        tags=["AI Jobs"],
        summary="Get a job by id",
        parameters=[OpenApiParameter("id", OpenApiTypes.STR, OpenApiParameter.PATH)],
        responses=JobSerializer,
    )
    def retrieve(self, request, id=None):
        # Stubbed example
        return Response({"id": id or "unknown", "status": "queued"})