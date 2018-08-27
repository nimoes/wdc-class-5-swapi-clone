import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

from api.models import Planet, People
from api.fixtures import SINGLE_PEOPLE_OBJECT, PEOPLE_OBJECTS
from api.serializers import serialize_people_as_json


def single_people(request):
    return JsonResponse(SINGLE_PEOPLE_OBJECT)


def list_people(request):
    return JsonResponse(PEOPLE_OBJECTS, safe=False)


@csrf_exempt
def people_list_view(request):
    """
    People `list` actions:

    Based on the request method, perform the following actions:

        * GET: Return the list of all `People` objects in the database.

        * POST: Create a new `People` object using the submitted JSON payload.

    Make sure you add at least these validations:

        * If the view receives another HTTP method out of the ones listed
          above, return a `400` response.

        * If submited payload is nos JSON valid, return a `400` response.
    """
    if request.method == 'GET':
        people = People.objects.all()
        myList = []
        for eachperson in people:
            myList.append(serialize_people_as_json(eachperson))
        return JsonResponse(myList, safe=False)
        
    elif request.method == 'POST':
        body = request.body.decode('utf-8')
        try:
            data = json.loads(body)
            print(data)
        except:
            return JsonResponse({
                "success": False,
                "msg": "Provided payload is not valid"
            }, status=400)
            
        planet_id = data['homeworld'].split('/')[-2]
        # check for valid planet
        try:
            planet = Planet.objects.get(id=planet_id)
        except Planet.DoesNotExist:
            return JsonResponse({
                "success": False,
                "msg": "Could not find planet with id: {}".format(planet_id)
            }, status=404)
        
        if type(data['height']) != int or type(data['mass']) != int:
            return JsonResponse({
                "success": False,
                "msg": "Provided payload is not valid"
            }, status=400)
        
        person = People.objects.create(
            name = data['name'],
            homeworld = planet,
            height = data['height'],
            mass = data['mass'],
            hair_color = data['hair_color'],
            created = data['created']
        )
        
        return JsonResponse(serialize_people_as_json(person), status=201)

    else:
        return JsonResponse({
            'err':'a bad request'
        }, status=400)

@csrf_exempt
def people_detail_view(request, people_id):
    """
    People `detail` actions:

    Based on the request method, perform the following actions:

        * GET: Returns the `People` object with given `people_id`.

        * PUT/PATCH: Updates the `People` object either partially (PATCH)
          or completely (PUT) using the submitted JSON payload.

        * DELETE: Deletes `People` object with given `people_id`.

    Make sure you add at least these validations:

        * If the view receives another HTTP method out of the ones listed
          above, return a `400` response.

        * If submited payload is nos JSON valid, return a `400` response.
    """

    
    try:
        person = People.objects.get(id=people_id)
    except People.DoesNotExist:
        return JsonResponse({
            'msg': 'ID does not exist',
            'success': False
        }, status=400)
        
    if request.method == 'GET':
        return JsonResponse(serialize_people_as_json(person), status=200)
    
    elif request.method == 'PATCH' or request.method == 'PUT':
        # edge cases
        try:
            body = request.body.decode('utf-8')
            data = json.loads(body)
        except:
            return JsonResponse({
                'msg': 'Provide a valid JSON payload',
                'success': False
            }, status=400)
        
        # check if planet exists
        try:
            planet_id = data['homeworld'].split('/')[-2]
            planet = Planet.objects.get(id=planet_id)
        except Planet.DoesNotExist:
            return JsonResponse({
                'msg': 'Could not find planet with id: {}'.format(planet_id),
                'success': False
            }, status=404)

        # check if height and mass are integers
        try:
            if type(data['height']) != int or type(data['mass']) != int:
                return JsonResponse({
                    "success": False,
                    "msg": "Provided payload is not valid"
                }, status=400)
        except KeyError:
            pass

        # if put (full update), ensure each field matches and exists in data
        if request.method == 'PUT':
            fields = ['name', 'height', 'mass', 'homeworld', 'hair_color']
            match = False
            if all(field in data.keys() for field in fields) and\
            len(set(data))-len(set(fields)) == 0:
                match = True
            else:
                return JsonResponse({
                    'msg': 'Missing field in full update',
                    'success': False
                }, status=400)

        for key, val in data.items():
            if key == 'homeworld':
                person.key = planet
            else:
                setattr(person, key, val)
            person.save()
        return JsonResponse(serialize_people_as_json(person), status=200)

    elif request.method == 'DELETE':
        try:
            person = People.objects.get(id=people_id)
        except People.DoesNotExist:
            return JsonResponse({
                'msg': 'Provide a valid JSON payload',
                'success': False
            }, status=400)
            
        person.delete()
        return JsonResponse({
            'msg': 'deleted {} from the database'.format(person.name),
            'success': True
        }, status=200)
        
    else:
        return JsonResponse({
            'msg': 'Invalid HTTP method',
            'success': False
        }, status=400)
    
