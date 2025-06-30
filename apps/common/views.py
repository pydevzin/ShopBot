import json

import redis
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.bot.config.run_bot import get_bot_and_dp

import logging

logger = logging.getLogger(__name__)

# Configure Redis connection
redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)


@api_view(["GET"])
def health_check_redis(request):
    try:
        # Check Redis connection
        redis_client.ping()
        return Response({"status": "success"}, status=status.HTTP_200_OK)
    except redis.ConnectionError:
        return Response(
            {"status": "error", "message": "Redis server is not working."},
            status=status.HTTP_400_BAD_REQUEST,
        )


@csrf_exempt
async def telegram_webhook(request):
    if request.method == "POST":
        try:
            logger.info(f"Webhook received: {request.body[:200]}")
            data = json.loads(request.body.decode('utf-8'))
            bot, dp = await get_bot_and_dp()
            await dp.feed_webhook_update(bot, data)
            return HttpResponse("ok")
        except Exception as e:
            logger.error(f"Webhook error: {str(e)}")
            return HttpResponse(f"Bad request: {str(e)}", status=400)
    return HttpResponse("Method not allowed", status=405)
