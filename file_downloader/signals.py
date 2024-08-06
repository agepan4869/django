import os
import logging
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import UploadedFile

# ロギング設定
logger = logging.getLogger(__name__)

@receiver(post_delete, sender=UploadedFile)
def delete_files(sender, instance, **kwargs):
    """
    UploadedFileモデルのインスタンスが削除された後に呼び出されるシグナルハンドラ。
    関連するファイルとサブディレクトリを削除します。
    
    :param sender: シグナルを送信したモデルクラス（この場合はUploadedFile）
    :param instance: 削除されたUploadedFileモデルのインスタンス
    :param kwargs: 追加のキーワード引数
    """
    logger.info(f"Triggered delete_files for instance {instance.id}")
    
    # ファイルの削除
    if instance.file:
        file_path = instance.file.path  # 削除するファイルのパスを取得
        logger.debug(f"File path: {file_path}")
        if os.path.isfile(file_path):  # ファイルが存在するか確認
            logger.info(f"Deleting file: {file_path}")
            os.remove(file_path)  # ファイルを削除
        else:
            logger.warning(f"File not found: {file_path}")
    
    # サブディレクトリの削除
    subdirectory_path = os.path.join(instance.file.storage.location, instance.subdirectory)
    logger.debug(f"Subdirectory path: {subdirectory_path}")
    if os.path.isdir(subdirectory_path) and not os.listdir(subdirectory_path):  # ディレクトリが存在し、空であることを確認
        logger.info(f"Deleting directory: {subdirectory_path}")
        os.rmdir(subdirectory_path)  # ディレクトリが空の場合のみ削除
    else:
        logger.warning(f"Directory not found or not empty: {subdirectory_path}")
