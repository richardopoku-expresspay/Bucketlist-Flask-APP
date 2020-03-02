from flask import request, jsonify, abort
from .models import BucketList


def baseResponse(message, data, error_code):
    result = {'message': message, 'error_code': error_code}
    if bool(data):
        result['data'] = data

    response = jsonify(result)
    response.status_code = error_code

    return response

def successResponse(message, data={}, error_code=200):
    return baseResponse(message, data, error_code)

def errorResponse(message, data={},  error_code=400):
    return baseResponse(message, data, error_code)

def bucketlists():
    if request.method == 'POST':
        name = str(request.data.get('name', ''))
        if name:
            bucketlist = BucketList(name=name)
            bucketlist.save()
            response = {
                'id': bucketlist.id,
                'name': bucketlist.name,
                'created_at': bucketlist.date_created,
                'updated_at': bucketlist.date_modified
            }

            return successResponse('Bucketlist created.', {'bucketlist': response}, 201)

    else:
        bucketlists = BucketList.get_all()
        results = []

        for bl in bucketlists:
            obj = {
                'id': bl.id,
                'name': bl.name,
                'created_at': bl.date_created,
                'updated_at': bl.date_modified
            }
            results.append(obj)

        return successResponse('Success', {'bucketlists': results})

def manipulations(id, **kwargs):
    bucketlist = BucketList.query.filter_by(id=id).first()
    if not bucketlist:
        abort(404)

    if request.method == 'DELETE':
        bucketlist.delete()
        return successResponse('Bucketlist {} has been deleted.'.format(id))
    elif request.method == 'PUT':
        name = str(request.data.get('name', '')) # get the name else default to ''
        bucketlist.name = name if name != '' else bucketlist.name
        bucketlist.save()
        
        response = {
            'id': bucketlist.id,
            'name': bucketlist.name,
            'created_at': bucketlist.date_created,
            'updated_at': bucketlist.date_modified
        }

        return successResponse('Success', {'bucketlist': response}, 200)
    else:
        response = {
            'id': bucketlist.id,
            'name': bucketlist.name,
            'created_at': bucketlist.date_created,
            'updated_at': bucketlist.date_modified
        }

        return successResponse('Success', {'bucketlist': response}, 200)