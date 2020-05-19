import pycurl, json
from .models import *
from io import BytesIO
from .serializers import *
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import ( HTTP_200_OK, HTTP_405_METHOD_NOT_ALLOWED )


@api_view(['GET'])
def dashboard(request):
    if request.method == 'GET':
        apps = AppDetailSerailizer(AppDetail.objects.filter(app2Monitor = True).order_by('id'), many=True)
        return render(request, 'applications.html', {"apps": apps.data})
    else:
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])      
def load_appData(request, application):
    if request.method == 'GET':
        appData = AppData.objects.filter(status_time__gt = (datetime.now() + timedelta(hours = -1 * settings.DATA_VIEW_HOURS))).filter(application=AppDetail.objects.get(Application=application).id).order_by('status_time')
        labels, data, backgroundColor, message = [], [], [], []
        for Data in appData:
            labels.append(Data.status_time)
            appMessage = ""
            if Data.status.lower() == 'ok':
                backgroundColor.append(settings.STATUS_SUCCESS_COLOR)
                data.append(1)
            else:
                backgroundColor.append(settings.STATUS_FAILURE_COLOR)
                data.append(0.5)
                serdata =  AppDataSerailizer(Data)
                for target in serdata.data["targets"]:
                    if target["status"].lower() == "fail":
                        appMessage = appMessage + target["target"] + " - " + target["message"] + ". "
            if len(appMessage) > 0:
                message.append(appMessage)
            else:
                message.append("ok")
        responseData = {"minBound": datetime.now() + timedelta(hours = -1 * settings.DATA_VIEW_HOURS), "maxBound": datetime.now(), "datasets": [{"data": data, "backgroundColor": backgroundColor, "message": message, "label": application}], "labels": labels}
        return Response(responseData, status=HTTP_200_OK)
    else:
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)

 
def scheduled_Job():
    apps = AppDetail.objects.filter(app2Monitor = True)
    for app in apps:
        try:
            buffer = BytesIO()
            c = pycurl.Curl()
            c.setopt(c.URL, app.appEndPoint)
            c.setopt(c.WRITEDATA, buffer)
            c.perform()
            c.close()
            data = json.loads(buffer.getvalue().decode('iso-8859-1'))
            data.update({"application": app.id})
            Appdata = AppDataLoadSerializer(data=data)
            if Appdata.is_valid():
                Appdataloaded = Appdata.save()
                for Tar in data["targets"]:
                    Tar.update({"targets": Appdataloaded.id})
                    Intdata = InterfaceLoadSerailizer(data = Tar)
                    if Intdata.is_valid():
                        Intdata.save()
        except Exception as sje:
            print (sje)
            pass
