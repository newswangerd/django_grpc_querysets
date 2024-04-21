from test_app import models

from rest_framework import serializers


class TestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TestModel
        fields = "__all__"
