from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


def image_upload_for_predict(request):
    if request.method == "POST" and request.FILES["image_file"]:
        image_file = request.FILES["image_file"]
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        image_url = fs.url(filename)
        print(image_url)
        return render(request, "uploadforpredict.html", {
            "image_url": image_url
        })
    return render(request, "uploadforpredict.html")
