from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from backend.settings import DEBUG, MEDIA_ROOT, MEDIA_UPLOAD_FOLDER

def image_upload_for_predict(request):
    if request.method == "POST" and request.FILES["image_file"]:
        image_file = request.FILES["image_file"]
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        image_url = fs.url(filename)
    
        if DEBUG:
            print(image_url)
    
        return render(request, "uploadforpredict.html", {
            "image_url": image_url
        })
    return render(request, "uploadforpredict.html")
