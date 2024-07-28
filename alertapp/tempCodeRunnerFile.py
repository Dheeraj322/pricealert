import asyncio
import json
import websockets
from celery import shared_task
from django.core.mail import send_mail
from .models import Alert
from django.conf import settings

alerts = Alert.objects.filter(status="active")
print(alerts.name)