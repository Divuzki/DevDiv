from django.http.request import HttpHeaders
from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
import requests
import json

from firebase_admin.messaging import Message
from fcm_django.models import FCMDevice

def send_notification(registration_ids, message_title, message_desc, message_image):
    # Send to multiple devices by passing a list of ids.
    registration_ids = []
    for id in registration_ids:
        registration_ids.append(id)

    fcm_api = "AAAALMmMJ1g:APA91bFuK6lbc2LAGz0-sb5slMpAvB0sBYHSEQ9VwzsFuoXaRtKMSfpao89HRQ6wuPYVSUu8leHtXlhnQ5k7kB0vq20kfIgapHBIL1Y6B-3UvHau5OTzImHU25tyM9ioAVs7gM4ITae3"
    url = "https://fcm.googleapis.com/fcm/send"

    headers = {
        "Content-Type": "application/json",
        "Authorization": 'key='+fcm_api}

    payload = {
        "registration_ids": registration_ids,
        "priority": "high",
        "notification": {
            "body": message_desc,
            "title": message_title,
            "image": message_image,
            "icon": "https://d2rkspfokjrj1j.cloudfront.net/static/logo.png",

        }
    }

    result = requests.post(url,  data=json.dumps(payload), headers=headers)
    print(result.json())


def index(request):
    return render(request, 'index.html')


def send(title="zazuu", content="te", image="ggg"):
    # message_obj = Message(
    #     data={
    #         "Nick" : "Mario",
    #         "body" : "great match!",
    #         "Room" : "PortugalVSDenmark"
    #    },
    # )

    # # You can still use .filter() or any methods that return QuerySet (from the chain)
    # device = FCMDevice.objects.all().first()
    # # send_message parameters include: message, dry_run, app
    # device.send_message(message_obj)
    # Boom!
    # resgistration = FCMDevice.objects.all().registration_id
    print(FCMDevice.objects.all())
    # send_notification(
    #     resgistration, str(title), str(content), str(image))
    return HttpResponse("sent")


def showFirebaseJS(request):
    template = get_template('webpush.js')
    html = template.render()
    return HttpResponse(html, content_type="application/x-javascript")
