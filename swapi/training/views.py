import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


def text_response(request):
    """
    Return a HttpResponse with a simple text message.
    Check that the default content type of the response must be "text/html".
    """
    return HttpResponse("a simple text message", content_type="text/html")


def looks_like_json_response(request):
    """
    Return a HttpResponse with a text message containing something that looks
    like a JSON document, but it's just "text/html".
    """
    return HttpResponse("{'received': True}", content_type="text/html")


def simple_json_response(request):
    """
    Return an actual JSON response by setting the `content_type` of the HttpResponse
    object manually.
    """
    obj = {
        'received': True
    }
    return HttpResponse(json.dumps(obj), content_type="application/json")


def json_response(request):
    """
    Return the same JSON document, but now using a JsonResponse instead.
    """
    return JsonResponse({'received': True})


def json_list_response(request):
    """
    Return a JsonReponse that contains a list of JSON documents
    instead of a single one.
    Note that you will need to pass an extra `safe=False` parameter to
    the JsonResponse object it order to avoid built-in validation.
    https://docs.djangoproject.com/en/2.0/ref/request-response/#jsonresponse-objects
    """
    obj_one = {
        'name': 'objectOne',
        'received': True
    }
    obj_two = {
        'name': 'objectTwo',
        'received': True
    }
    return JsonResponse([obj_one, obj_two], safe=False)

def json_error_response(request):
    """
    Return a JsonResponse with an error message and 400 (Bad Request) status code.
    """
    return JsonResponse({'err': 'bad request'}, status=400)


@csrf_exempt
def only_post_request(request):
    """
    Perform a request method check. If it's a POST request, return a message saying
    everything is OK, and the status code `200`. If it's a different request
    method, return a `400` response with an error message.
    """
    if request.method == 'POST':
        return HttpResponse('everything is OK', status=200)
    else:
        return HttpResponse('bad request', status=400)


@csrf_exempt
def post_payload(request):
    """
    Write a view that only accepts POST requests, and processes the JSON
    payload available in `request.body` attribute.
    """
    if request.body and request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        return JsonResponse({'status': 'ok'}, status=200)
    else:
        return JsonResponse({'err': 'only POST request is allowed'}, status=400)


def custom_headers(request):
    """
    Return a JsonResponse and add a custom header to it.
    """
    resp = JsonResponse({'status': 'ok'}, status=201)
    resp['custom-header'] = 'randome value'
    
    return resp


def url_int_argument(request, first_arg):
    """
    Write a view that receives one integer parameter in the URL, and displays it
    in the response text.
    """
    return HttpResponse("a chosen integer is : {}".format(first_arg))


def url_str_argument(request, first_arg):
    """
    Write a view that receives one string parameter in the URL, and displays it
    in the response text.
    """
    return HttpResponse("a chosen string is : '{}'".format(first_arg))


def url_multi_arguments(request, first_arg, second_arg):
    """
    Write a view that receives two parameters in the URL, and display them
    in the response text.
    """
    return JsonResponse({
        'first parameter': first_arg,
        'second parameter': second_arg
    })


def get_params(request):
    """
    Write a view that receives GET arguments and display them in the
    response text.
    """
    return JsonResponse(request.GET)
