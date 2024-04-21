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
        query_pb2_grpc.add_RemoteQuerysetServicer_to_server(
            QueryServer({"test": serializers.TestModelSerializer}), server
        )
        server.add_insecure_port("[::]:" + port)
        server.start()
        print("Server started, listening on " + port)
        server.wait_for_termination()
