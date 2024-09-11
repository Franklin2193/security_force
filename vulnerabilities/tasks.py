# vulnerabilities/tasks.py

from celery import shared_task
from django.core.cache import cache
import requests

@shared_task
def update_vulnerabilities_cache():
    url = 'https://services.nvd.nist.gov/rest/json/cves/2.0'
    params = {
        'resultsPerPage': 20,  # Traer solo 20 registros por vez
        'startIndex': 0
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json().get('vulnerabilities', [])
    cache.set('vulnerabilities_data', data, timeout=3600)

