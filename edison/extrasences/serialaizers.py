from rest_framework import serializers
from .models import *
import json
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from io import BytesIO


class GamerSerializer(serializers.Serializer):
    numbers_history = serializers.ListField()
    last_num = serializers.IntegerField(max_value=99, min_value=10)

    def create(self, validated_data):
        return Gamer(**validated_data)

    def save_to_session(self, request):
        content = json.dumps(self.data)
        request.session['data']['gamer'] = content
        request.session.modified = True

    def create_from_session(self, request):
        if 'data' in request.session and 'gamer' in request.session['data']:
            content = request.session['data']['gamer']
            data = json.loads(content)
            self.__init__(data=data)
            self.is_valid()
            if self.is_valid():
                return self.create(self.validated_data)


class ExtraSerializer(serializers.Serializer):
    name = serializers.CharField(allow_blank=True)
    level = serializers.IntegerField()
    numbers_history = serializers.ListField()
    last_num = serializers.IntegerField(max_value=99, min_value=10)

    def create(self, validated_data):
        return Extra(**validated_data)

    def save_to_session(self, request):
        content = json.dumps(self.data)
        name = self.data['name']
        if 'data' in request.session:
            if 'extra' in request.session['data'] and isinstance(request.session['data']['extra'], dict):
                request.session['data']['extra'].update({name: content})
            else:
                request.session['data'].update({'extra': {name: content}})
        else:
            request.session['data'] = {'extra': {name: content}}
        request.session.modified = True

    def create_from_session(self, request):
        extra_dict = {}
        if 'data' in request.session:
            content = request.session['data']['extra']
            for extra in content:
                data = json.loads(content[extra])
                extra_dict[data['name']] = self.create(data)
            return extra_dict
