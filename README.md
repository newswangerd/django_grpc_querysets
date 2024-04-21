# gRPC Querysets

This library provides a gRPC client and server that allows for Django querysets to be executred remotetly.

## Demo

### Server
Create a management command for running the gRPC process:

```python
from concurrent import futures

import grpc
from django.core.management.base import BaseCommand
from grpc_querysets.server import QueryServer
from grpc_querysets.lib import query_pb2_grpc

from test_app import serializers


class Command(BaseCommand):

    def handle(self, *args, **options):
        port = "50051"
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        # Registers type "test" with TestModelSerializer
        query_pb2_grpc.add_RemoteQuerysetServicer_to_server(
            QueryServer({"test": serializers.TestModelSerializer}), server
        )
        server.add_insecure_port("[::]:" + port)
        server.start()
        print("Server started, listening on " + port)
        server.wait_for_termination()
```

Launch the gRPC server with `$ python manage.py start_grpc_server`

### Client

With the server set up, we can now interract with our Django app using an API client that mimics the Django queryset API.


```
$ python manage.py shell

>>> from test_app import serializers
>>> from grpc_querysets.grpc_queryset import RemoteQueryset
>>> qs = RemoteQueryset(serializers.TestModelSerializer, "test")

>>> qs.create(name="foo", f1="other field")
sending request
request finished in 0.008120059967041016 seconds
{'name': 'foo', 'f1': 'other field', 'f2': None, 'my_fk': None}

>>> qs.count()
sending request
request finished in 0.005173921585083008 seconds
1

>>> qs.create(name="foo2")
sending request
request finished in 0.008412837982177734 seconds
{'name': 'foo2', 'f1': None, 'f2': None, 'my_fk': None}

>>> qs.create(name="my_name")
sending request
request finished in 0.006021261215209961 seconds
{'name': 'my_name', 'f1': None, 'f2': None, 'my_fk': None}

>>> list(qs.all())
sending request
request finished in 0.006189823150634766 seconds
request finished in 0.0001957416534423828 seconds
request finished in 0.00018596649169921875 seconds
[{'name': 'foo', 'f1': 'other field', 'f2': None, 'my_fk': None}, {'name': 'foo2', 'f1': None, 'f2': None, 'my_fk': None}, {'name': 'my_name', 'f1': None, 'f2': None, 'my_fk': None}]

>>> list(qs.exclude(name__icontains="foo"))
sending request
request finished in 0.00799417495727539 seconds
[{'name': 'my_name', 'f1': None, 'f2': None, 'my_fk': None}]

>>> list(qs.filter(name__icontains="foo"))
sending request
request finished in 0.005292177200317383 seconds
request finished in 0.00015282630920410156 seconds
[{'name': 'foo', 'f1': 'other field', 'f2': None, 'my_fk': None}, {'name': 'foo2', 'f1': None, 'f2': None, 'my_fk': None}]

>>> qs.filter(name__icontains="foo").count()
sending request
request finished in 0.006677865982055664 seconds
2

>>> qs.all().delete()
sending request
request finished in 0.009694814682006836 seconds

>>> qs.count()
sending request
request finished in 0.004435062408447266 seconds
0
```