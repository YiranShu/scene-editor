import os
from django.shortcuts import render
from django.http import HttpResponse
import datetime
from . import models


def upload(request):
    return render(request, 'uploader/upload.html', {})


def save_to_database(request):
    if request.method == "POST":
        myFile = request.FILES.get("myfile", None)
        if not myFile:
            return HttpResponse("no files for upload!")

        scene = models.Scene(
            file=myFile, 
            file_name=myFile.name,
            scene_name=request.POST.get("scene_name"),
            description=request.POST.get("description"),
            category=request.POST.get("category"),
            tag=request.POST.get("tag"),
            date_created=datetime.datetime.now()
        ).save()
        print(type(request.POST.get("scene_name")))
        return HttpResponse(myFile.name + " upload over!")


def retrieve_from_database(request, scene_id):
    scenes = models.Scene.objects(file_name=scene_id)
    print(len(scenes))
    for scene in scenes:
        file = scene.file

        destination = open(os.path.join("/Users/lewislin/Downloads/", scene.file_name), 'wb+')
        chunk = file.read(size=4000)

        while chunk:
            destination.write(chunk)
            chunk = file.read(size=4000)

        destination.close()
        print(scene.scene_name)
        output = scene.scene_name + " " + scene.description + " " + scene.category + " " +scene.tag + " " + str(scene.date_created)
        
    return HttpResponse(scene_id + " has been saved! " + output)

