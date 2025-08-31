from django.apps import AppConfig
import asyncio
import os


class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.bot'
    verbose_name = 'Telegram Bot'

    def ready(self):
        """Reset webhook when Django starts"""
        if os.environ.get('RUN_MAIN', None) != 'true':  # Prevent running twice in development
            return
            
        try:
            from django.conf import settings
            from .utils import register_bot_webhook
            
            bot_token = getattr(settings, 'BOT_TOKEN', None)
            webhook_url = getattr(settings, 'WEBHOOK_URL', 'http://localhost:8000')
            
            if bot_token and webhook_url.startswith('https://'):
                # Only set webhook if we have HTTPS URL
                full_webhook_url = f"{webhook_url}/api/bot"
                asyncio.run(register_bot_webhook(bot_token, full_webhook_url))
                print(f"✅ Bot webhook reset to: {full_webhook_url}")
            elif bot_token:
                print(f"⚠️ Skipping webhook registration: HTTPS URL required, got: {webhook_url}")
                print(f"💡 For development, use ngrok or set WEBHOOK_URL to HTTPS URL")
        except Exception as e:
            print(f"⚠️ Failed to reset bot webhook: {e}")
