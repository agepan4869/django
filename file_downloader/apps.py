from django.apps import AppConfig

class FileDownloaderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'file_downloader'

    def ready(self):
        import file_downloader.signals  # シグナルのインポート
