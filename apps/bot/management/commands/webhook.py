import requests
from django.core.management.base import BaseCommand
from django.conf import settings




def get_bot_webhook_single2(bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
    r = requests.post(url)
    return r.json()


def get_bot_info_single2(bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    response = requests.post(url)
    return response.json().get("result").get("username"), response.status_code


def get_webhook():
    bot = getattr(settings, 'BOT_TOKEN', None)

    username, res = get_bot_info_single2(bot)
    print("\n\n", 100 * "-")
    print("webhook info get for bot:", f"https://t.me//{username}")
    print("token:", bot, "status:", res)
    print("webhook url:", get_bot_webhook_single2(bot))
    print("Get webhook info successfully for all bots\n\n")


def get_bot_info_single(bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    response = requests.post(url)
    return response.json().get("result").get("username")


def set_webhook_single(bot_token, webhook_url):
    url_webhook = f"{webhook_url}/api/bot"
    print("url_webhook", url_webhook)
    url = (
        f"https://api.telegram.org/bot{bot_token}/setWebhook?url={url_webhook}"
    )
    response = requests.post(url)
    return response


def get_bot_webhook_single(bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
    r = requests.post(url)
    return r.json()


def set_webhook():
    bot = getattr(settings, 'BOT_TOKEN', None)

    res = set_webhook_single(bot, settings.WEBHOOK_URL)
    username = get_bot_info_single(bot)
    print("\n\n", 100 * "-")
    print("webhook set for bot:", f"https://t.me//{username}")
    print("token:", bot, "status:", res.status_code)
    print("webhook url:", get_bot_webhook_single(bot).get("result").get("url"))
    print("Webhook set successfully for all bots\n\n")

def delete_webhook():
    bot = getattr(settings, 'BOT_TOKEN', None)
    res = delete_webhook_single(bot, settings.WEBHOOK_URL)

def delete_webhook_single(bot_token, webhook_url):
    # BU YERDA XATO! "deleteWebhookInfo" degan endpoint mavjud emas.
    url = f"https://api.telegram.org/bot{bot_token}/deleteWebhook"
    res = requests.post(url)
    print("delete:",res)
    return res.json()

class Command(BaseCommand):
    help = "Set webhook for all bots"

    def handle(self, *args, **options):
        delete_webhook_single(settings.BOT_TOKEN, settings.WEBHOOK_URL)
        set_webhook()
        get_webhook()
