from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import View  # Add this line
from .models import Vulnerability
from .serializers import VulnerabilitySerializer
import requests  # Add this line
import json
from django.db.models import Count, Func
from .utils import fetch_vulnerabilities, save_vulnerabilities
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render

def home(request):
    return render(request, 'vulnerabilities/home.html')

class VulnerabilityPagination(PageNumberPagination):
    page_size = 20  # Número de registros por página
    page_size_query_param = 'resultsPerPage'
    max_page_size = 1000

class VulnerabilityListView(generics.ListAPIView):
    serializer_class = VulnerabilitySerializer
    pagination_class = VulnerabilityPagination

    def get_queryset(self):
        # Obtener vulnerabilidades de la API externa
        data = fetch_vulnerabilities()

        # Guardar o actualizar vulnerabilidades en la base de datos
        save_vulnerabilities(data)

        # Devolver todas las vulnerabilidades desde la base de datos
        return Vulnerability.objects.all()

class FixedVulnerabilitiesView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data  # DRF maneja automáticamente la conversión de JSON
            cve_ids = data.get('cve_ids', [])
            if not cve_ids:
                return Response({"error": "No CVE IDs provided"}, status=status.HTTP_400_BAD_REQUEST)

            # Actualizar las vulnerabilidades como fixed
            updated_count = Vulnerability.objects.filter(cve_id__in=cve_ids).update(fixed=True)
            return Response({"status": "success", "updated_count": updated_count})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

def mark_vulnerabilities_fixed(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cve_ids = data.get('cve_ids', [])
            if not cve_ids:
                return JsonResponse({"status": "error", "message": "No CVE IDs provided"}, status=400)

            updated_count = Vulnerability.objects.filter(cve_id__in=cve_ids).update(fixed=True)
            return JsonResponse({"status": "success", "updated_count": updated_count})

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

class ActiveVulnerabilitiesView(generics.ListAPIView):
    serializer_class = VulnerabilitySerializer

    def get_queryset(self):
        return Vulnerability.objects.filter(fixed=False)

class Lowercase(Func):
    function = 'LOWER'

class VulnerabilitySummaryView(APIView):
    def get(self, request, *args, **kwargs):
        # Normalizar severidades a minúsculas y agrupar
        summary = (Vulnerability.objects
                   .annotate(lower_severity=Lowercase('severity'))  # Normalizar severidad a minúsculas
                   .values('lower_severity')  # Agrupamos por severidad normalizada
                   .annotate(count=Count('id'))  # Contamos el número de vulnerabilidades para cada severidad
                   .order_by('lower_severity'))  # Ordenamos por severidad normalizada

        # Convertir a formato de respuesta
        summary_data = [{'severity': item['lower_severity'], 'count': item['count']} for item in summary]

        return Response(summary_data)
