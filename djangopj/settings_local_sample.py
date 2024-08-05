SECRET_KEY = ''


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_docker',
        'USER': 'django',
        'PASSWORD': 'django',
        'HOST': 'db',
        'POST': '3306'
    }
}