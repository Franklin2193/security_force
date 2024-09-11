# security_force/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establece el módulo de configuración de Django para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'security_force.settings')

app = Celery('security_force')

# Carga configuraciones de Celery desde el archivo de configuración de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubre tareas en todos los módulos de tareas de Django
app.autodiscover_tasks()

# Opcional: configuración de Celery Beat para tareas periódicas
from celery.schedules import crontab

app.conf.beat_schedule = {
    'update-vulnerabilities-cache-every-hour': {
        'task': 'vulnerabilities.tasks.update_vulnerabilities_cache',
        'schedule': crontab(minute=0, hour='*/1'),  # Cada hora
    },
}
