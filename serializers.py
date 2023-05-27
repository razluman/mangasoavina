from rest_framework import serializers
from .models import Apv


class ApvSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='paroasy:apv-detail')

    class Meta:
        model = Apv
        fields = ['url', 'apv', 'mpiaro', 'fankalazana']
