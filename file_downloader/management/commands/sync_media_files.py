import os
from django.core.management.base import BaseCommand
from django.conf import settings
from file_downloader.models import UploadedFile

class Command(BaseCommand):
    help = 'Sync media files with the database'

    def handle(self, *args, **kwargs):
        media_root = settings.MEDIA_ROOT
        
        # サーバー上のファイルをチェック
        server_files = set()
        for root, dirs, files in os.walk(media_root):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, media_root)
                server_files.add(relative_path)

                # ファイルが既に存在するか確認
                if not UploadedFile.objects.filter(file=relative_path).exists():
                    subdirectory, filename = os.path.split(relative_path)
                    UploadedFile.objects.create(
                        subdirectory=subdirectory,
                        file=relative_path
                    )
                    self.stdout.write(self.style.SUCCESS(f'Added: {relative_path}'))
                else:
                    self.stdout.write(f'Already exists: {relative_path}')

        # データベース上のエントリをチェック
        db_files = set(UploadedFile.objects.values_list('file', flat=True))
        for db_file in db_files:
            if db_file not in server_files:
                UploadedFile.objects.filter(file=db_file).delete()
                self.stdout.write(self.style.WARNING(f'Removed: {db_file}'))
