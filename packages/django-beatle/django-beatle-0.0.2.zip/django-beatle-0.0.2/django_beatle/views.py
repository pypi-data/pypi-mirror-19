from functools import wraps
import hmac
import importlib

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from .conf import settings
from .models import Task


def get_signature(params=None):
    if params is None:
        params = {}

    msg = ''.join(map(str, sorted(params.values()))).encode()
    return hmac.new(settings.SECRET_KEY.encode(), msg=msg).hexdigest()


def validate_signature(view):

    @wraps(view)
    def wrapped(request, *args, **kwargs):
        if request.GET.get('SIGNATURE') != get_signature(request.POST.dict()):
            return HttpResponseBadRequest()

        return view(request, *args, **kwargs)

    return wrapped


@validate_signature
@csrf_exempt
def endpoint(request):
    if request.method == 'GET':
        configuration = settings.get_configuration()
        return JsonResponse(configuration)

    response = 'OK'
    task = request.POST.get('TASK', '').strip('\'\"')
    try:
        db_task = Task.objects.get(path=task)
        if not db_task.is_enabled:
            response = 'Task disabled'

        else:
            str_module, str_function = task.rsplit('.', 1)
            module = importlib.import_module(str_module)
            getattr(module, str_function)()
    except Exception as e:
        response = str(e)

    return JsonResponse({'response': response})
