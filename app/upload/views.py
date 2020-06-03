from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from backend.settings import DEBUG, MEDIA_ROOT, MEDIA_UPLOAD_FOLDER

import os

def image_upload(request):
    
    if request.method == "POST" and request.FILES["image_file"]:
        image_file = request.FILES["image_file"]
        fs = FileSystemStorage()
        img_fpath = os.path.join('websiteupload', image_file.name)
        filename = fs.save(img_fpath, image_file)
        image_url = fs.url(filename)
        print(image_url)
        context = {
            "image_url": image_url,
            "image_name": image_file.name
        }
        return render(request, "upload.html", context=context)
        
    page_title='Predict'
    
    context = {
        "page_title":page_title,
        "image_name": 'select an image'
    }
    return render(request, "upload.html", context=context)
