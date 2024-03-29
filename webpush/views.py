import json
import requests
from django.conf import settings
# from django.shortcuts import render
from .models import WebPushNotificationUsers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

STATIC_URL = settings.STATIC_URL


def send_notification(registration_ids, message_title, message_desc, message_image, message_link):
    fcm_api = "AAAALMmMJ1g:APA91bFuK6lbc2LAGz0-sb5slMpAvB0sBYHSEQ9VwzsFuoXaRtKMSfpao89HRQ6wuPYVSUu8leHtXlhnQ5k7kB0vq20kfIgapHBIL1Y6B-3UvHau5OTzImHU25tyM9ioAVs7gM4ITae3"
    url = "https://fcm.googleapis.com/fcm/send"

    headers = {
        "Content-Type": "application/json",
        "Authorization": 'key='+fcm_api}

    payload = {
        "registration_ids": registration_ids,
        "priority": "high",
        "from": "DevDiv NG",
        "notification": {
            "tag": "Latest News",
            "title": str(message_title),
            "body": str(message_desc),
            "image": message_image,
            "icon": "https://d2rkspfokjrj1j.cloudfront.net/static/favicon-32x32.png",
            "click_action": message_link,
            "sound": "https://d2rkspfokjrj1j.cloudfront.net/static/audio/notify-male-audio.wav"
        }
    }

    result = requests.post(url,  data=json.dumps(payload), headers=headers)
    print(result.json())


def send(request):
    resgistration = []
    qs = WebPushNotificationUsers.objects.all()
    for device in qs:
        resgistration.append(device.registration_id)
    send_notification(
        resgistration, 'Ignore', 'Ignore This', "https://d2rkspfokjrj1j.cloudfront.net/static/logo.png", "//devdiv.herokuapp.com")
    return HttpResponse("sent")


@csrf_exempt
def add_devices_view(request):
    response = HttpResponse("[WARN] Nothing Was Done 💔")
    if request.method == "POST":
        reg_id = request.POST.get("regId")
        type = request.POST.get("type")
        qs = WebPushNotificationUsers.objects.create(
            registration_id=reg_id, type=type)
        qs.save()
        response = HttpResponse("[INFO] Device Has Been Added!")
    return response
