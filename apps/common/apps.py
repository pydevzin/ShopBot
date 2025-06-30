import os
from pathlib import Path
import environ
import requests
import threading
from django.apps import AppConfig
from apps.bot.config.bot_config import WEBHOOK_URL

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))
BOT_TOKEN = env.str("BOT_TOKEN")


class CommonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.common"

    def ready(self):

        if not BOT_TOKEN or not WEBHOOK_URL:
            print("BOT_TOKEN yoki WEBHOOK_URL topilmadi")
            return

        def set_webhook():
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
            data = {"url": WEBHOOK_URL}
            try:
                resp = requests.post(url, data=data)
                print(f"setWebhook javobi: {resp.text}")
            except Exception as e:
                print(f"setWebhook xatolik: {e}")

        threading.Thread(target=set_webhook, daemon=True).start()
