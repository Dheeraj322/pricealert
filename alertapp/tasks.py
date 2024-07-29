import redis
import os
import django
from celery import shared_task
from django.core.mail import send_mail
from .models import Alert


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pricealert.settings")
django.setup()
redis_client = redis.StrictRedis(host="redis", port=6379, db=0, decode_responses=True)


@shared_task
def alert_email(item, target_price, current_price, user_email):
    send_mail(
        subject="Price Alert Triggered",
        message=f"The price of {item} has reached your target price of {target_price}. Current price is {current_price}.",
        from_email="extrathrwaway@gmail.com",
        recipient_list=[user_email],
        fail_silently=False,
    )


@shared_task
def process_alerts():
    print("Starting process_alerts task.")
    alerts = Alert.objects.filter(status="created")
    if not alerts.exists():
        print("No alerts found with status 'created'.")
        return

    for alert in alerts:
        print(
            f"Processing alert for {alert.item} with target price {alert.target_price}."
        )

        try:
            current_price = float(redis_client.get(alert.item) or 0)
            current_price_db = float(alert.current_price or 0)
        except ValueError:
            print(f"Error converting price for {alert.item} to float.")
            current_price = 0

        target_price = float(alert.target_price or 0)

        print(f"Current price for {alert.item} is {current_price}.")
        print(f"Target price for {alert.item} is {target_price}.")

        if (current_price_db < target_price and current_price >= target_price and alert.status != "triggered") or (current_price_db > target_price and current_price <= target_price and alert.status != "triggered"):
            alert.status = "triggered"
            alert.save()
            print(
                f"Alert triggered for {alert.item} at target price {target_price}. Sending email to {alert.user.email}."
            )
            alert_email.delay(alert.item, target_price, current_price, alert.user.email)
        else:
            print(f"Alert not triggered for {alert.item}.")
