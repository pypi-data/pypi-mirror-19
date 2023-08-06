SECRET_KEY = 'fake-key'

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "analytics_kits",
    "tests",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test_database',
    }
}
