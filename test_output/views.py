import os
import datetime
import pandas as pd
from django.conf import settings
from django.http import HttpResponse
from django.core.management import call_command
from django.shortcuts import redirect

def export_excel(request):
    now = datetime.datetime.now()
    data = [
        {
            'Name': 'hoge',
            'Age': 20,
            'City': 'New York',
        },
        {
            'Name': 'fuga',
            'Age': 30,
            'City': 'London',
        }
    ]

    df = pd.DataFrame(data)
    
    # ディレクトリが存在しない場合は作成
    directory = os.path.join(settings.MEDIA_ROOT, 'TestDir')
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    file_path = os.path.join(directory, f'test_{now.strftime("%Y_%m_%d_%H_%M_%S")}.xlsx')
    df.to_excel(file_path)
    
    call_command('sync_media_files')

    return redirect('top_page')
