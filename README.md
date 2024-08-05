# 使い方
`sudo docker-compose build`  
`sudo docker-compose up -d`  
`sudo docker-compose run web python manage.py migrate`  
`docker-compose exec web python manage.py createsuperuser`

# IP制限のかけ方
djangopj > allow_IPs.pyを作成  
ALLOWED_IPSをリスト形式で定義し、許可IPをstr形式で追記していく