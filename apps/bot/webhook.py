# webhook.py (Corrected)
import json
import logging

from asgiref.sync import sync_to_async
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update

from .handler import get_application

logger = logging.getLogger(__name__)


@csrf_exempt
async def bot_webhook(request):
    print(request.body)
    update = Update.de_json(await request.read())
    """
    Receives webhook requests from Telegram, validates them, and passes
    the update to the application for processing either directly or via Celery.
    """
    # Get bot token from settings
    bot_token = getattr(settings, 'BOT_TOKEN', None)
    if not bot_token:
        return JsonResponse({"status": "bot token not configured"}, status=500)

    if request.method != "POST":
        return JsonResponse({"status": "invalid request"}, status=400)

    try:
        data = json.loads(request.body.decode("utf-8"))
        print(data)
    except json.JSONDecodeError:
        logger.warning("Received invalid JSON in webhook")
        return JsonResponse({"status": "invalid json"}, status=400)

    # Process the update directly in the main thread
    application = get_application(bot_token)

    update = Update.de_json(data, application.bot)
    await application.initialize()
    await application.process_update(update)

    return JsonResponse({"status": "ok"})