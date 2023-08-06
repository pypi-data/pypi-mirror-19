# django-beatle

Django client for [beatle](https://github.com/zhebrak/beatle)

#### Installation
```
pip install django-beatle
```

#### Configuration

Add `django_beatle` to `INSTALLED_APPS`
```python
INSTALLED_APPS = (
    ...
    'django_beatle'
)
```

Update `urls.py`
```python
url(r'^beatle/', include('django_beatle.urls')),
```

Create `beatleconf.py` in `settings.py` directory
```python
SECRET_KEY = <your secret key>

TASKS = {
    'example.views.stats': '*/2 * * * *',
    'example.views.another': '*/3 * * * *'
}

```
