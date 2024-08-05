from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import FileResponse
from .models import UploadedFile
from .forms import FileUploadForm
from django.core.files.storage import default_storage
from django.conf import settings
import os

def file_list(request):
    # メディアルートのトップレベルのディレクトリとファイルのリストを取得
    media_root = settings.MEDIA_ROOT
    directories = []
    files = []
    for entry in os.scandir(media_root):
        if entry.is_dir():
            directories.append(entry.name)
        elif entry.is_file():
            file_obj = UploadedFile.objects.filter(file=entry.name).first()
            if file_obj:
                files.append((file_obj.id, entry.name))
    return render(request, 'file_downloader/file_list.html', {'directories': directories, 'files': files})

def directory_files(request, directory):
    # 指定されたディレクトリ内のサブディレクトリとファイルを取得
    target_dir = os.path.join(settings.MEDIA_ROOT, directory)
    subdirectories = []
    files = []
    if os.path.exists(target_dir):
        for entry in os.scandir(target_dir):
            if entry.is_dir():
                subdirectories.append(entry.name)  # ここでディレクトリ名だけを取得
            elif entry.is_file():
                file_obj = UploadedFile.objects.filter(file=os.path.join(directory, entry.name)).first()
                if file_obj:
                    files.append((file_obj.id, entry.name))
    return render(request, 'file_downloader/directory_files.html', {
        'subdirectories': subdirectories,
        'files': files,
        'directory': directory
    })

def upload_file(request):
    default_directory = "Uploads"
    
    if request.method == 'POST':
        directory = request.POST.get('directory', default_directory)
        file = request.FILES['file']
        file_path = os.path.join(settings.MEDIA_ROOT, directory, file.name)

        # ディレクトリが存在しない場合は作成
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # ファイルを保存
        with default_storage.open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # データベースにファイル情報を保存
        uploaded_file = UploadedFile(file=os.path.join(directory, file.name))
        uploaded_file.save()

        return redirect('file_list')

    return render(request, 'file_downloader/upload_file.html', {'default_directory': default_directory})

def download_file(request, file_id):
    # ファイルのダウンロードロジック（例）
    file = get_object_or_404(UploadedFile, id=file_id)
    file_path = os.path.join(settings.MEDIA_ROOT, file.file.name)
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="application/force-download")
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
        return response