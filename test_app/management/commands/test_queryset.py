from __future__ import print_function

from django.core.management.base import BaseCommand
from test_app import serializers
from grpc_querysets.grpc_queryset import RemoteQueryset


import time


class Command(BaseCommand):
    help = "Launch gRPC auth service for envoy."

    def handle(self, *args, **options):
        start = time.time()
        qs = RemoteQueryset(serializers.TestModelSerializer, "test")

        qs.filter(name__icontains="x")

        print(qs)

        print(qs.count())

        print(time.time() - start)

        print(qs.create(name="foo", f1="bar", f2="foobar", my_fk=1))

        print(qs.count())
