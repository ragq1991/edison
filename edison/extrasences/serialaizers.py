from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import json


class SessionSerializer(serializers.Serializer):
    @staticmethod
    def fr(request):
        if 'data' in request.session:
            return json.loads(request.session['data'])
        return {}

    @staticmethod
    def to(request, data):
        request.session['data'] = json.dumps(data)
