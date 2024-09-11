from django.core.cache import cache
import requests
from .models import Vulnerability

def fetch_vulnerabilities():
    # Intenta obtener los datos del caché
    data = cache.get('vulnerabilities_data')

    if not data:
        # Si no hay datos en el caché, realiza la solicitud a la API
        url = 'https://services.nvd.nist.gov/rest/json/cves/2.0'
        params = {
            'resultsPerPage': 1550,  # Ingresar la cantidad de registros que se desea cargar de la url
            'startIndex': 0
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json().get('vulnerabilities', [])


        cache.set('vulnerabilities_data', data, timeout=3600)

    return data

def save_vulnerabilities(data):
    for item in data:
        cve_id = item['cve']['id']
        description = item['cve'].get('descriptions', [{}])[0].get('value', '')


        metrics = item['cve'].get('metrics', {})
        cvss_metric_v2 = metrics.get('cvssMetricV2', [{}])
        severity = cvss_metric_v2[0].get('baseSeverity', 'Unknown')


        references = item['cve'].get('references', [])
        fixed = any(reference.get('url') for reference in references)


        print(f"References: {references}")
        print(f"Fixed: {fixed}")

        if not references:
            fixed = False

        Vulnerability.objects.update_or_create(
            cve_id=cve_id,
            defaults={
                'description': description,
                'severity': severity,
                'fixed': fixed
            }
        )
