from django.shortcuts import render
from django.urls import get_resolver, NoReverseMatch, reverse

# URLパターン名と日本語表示名のマッピング辞書
URL_NAME_TO_JAPANESE = {
    'file_list': 'ファイル一覧',
    'upload_file': 'ファイルアップロード',
    'top_page': 'トップページ',
}

EXCLUDE_URL = [
    'top_page',
    'upload_file'
]

# 再帰的にURLパターンを取得する関数
def get_all_urls(patterns=None, namespace=None):
    if patterns is None:
        patterns = get_resolver().url_patterns

    all_urls = []
    for pattern in patterns:
        if hasattr(pattern, 'url_patterns'):
            # 再帰的に取得
            all_urls.extend(get_all_urls(pattern.url_patterns, namespace=pattern.namespace))
        elif hasattr(pattern, 'name') and pattern.name:
            name = f"{namespace}:{pattern.name}" if namespace else pattern.name
            try:
                # 'admin'名前空間および'top_page'を除外
                if not name.startswith('admin:') and name not in  EXCLUDE_URL:
                    # URLの逆解決が成功するか確認
                    reverse(name)
                    all_urls.append({
                        'name': name,
                        'pattern': pattern.pattern,
                        'japanese_name': URL_NAME_TO_JAPANESE.get(name, name)  # 日本語表示名を追加
                    })
            except NoReverseMatch:
                # 逆解決が失敗する場合はスキップ
                continue
    return all_urls

def top_page(request):
    urls = get_all_urls()
    return render(request, 'index.html', {'urls': urls})
