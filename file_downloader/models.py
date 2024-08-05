from django.db import models
import os

def upload_to_dynamic_subdirectory(instance, filename):
    return f'{instance.subdirectory}/{filename}'  # サブディレクトリ名を動的に設定

class UploadedFile(models.Model):
    subdirectory = models.CharField(max_length=255, default='Output')  # デフォルト値を追加
    file = models.FileField(upload_to=upload_to_dynamic_subdirectory)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    @property
    def filename(self):
        return os.path.basename(self.file.name)
