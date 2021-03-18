from rest_framework import serializers

from . import models


class CarSerializer(serializers.ModelSerializer):
    avg = serializers.IntegerField(read_only=True)
    class Meta:
        model = models.Car
        fields = '__all__'
        read_only_fields = (
            'avg',
        )


class PopularSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()
    class Meta:
        model = models.Car
        fields = '__all__'
        read_only_fields = (
            'count',
        )

class RateSerializer(serializers.ModelSerializer):
    #car = CarSerializer()
    class Meta:
        model = models.Rate
        fields = '__all__'
