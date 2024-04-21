from __future__ import print_function

import logging

import grpc
from grpc_querysets.lib.query_pb2 import Query, Action, Response
from grpc_querysets.lib import query_pb2_grpc
from google.protobuf.json_format import MessageToDict

from test_app import serializers

from google.protobuf.struct_pb2 import Struct
import time


def to_struct(data: dict) -> Struct:
    s = Struct()
    s.update(data)
    return s


class GRPCConnection:

    def single_request(self, request: Query):
        print("sending request")
        start = time.time()
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = query_pb2_grpc.RemoteQuerysetStub(channel)
            for response in stub.SingleQuery(request):
                # print("got response ")
                # print(MessageToDict(x))
                # data = serializers.TestModelSerializer(data=MessageToDict(x)["data"])
                # data.is_valid()
                print("request finished in " + str(time.time() - start) + " seconds")
                yield (response)
                start = time.time()


class RemoteObject(GRPCConnection):
    def __init__(self, serializer):
        self.data = serializer

    def __repr__(self):
        return str(self.data.data)

    # def save(self):
    #     data = {}
    #     for field in self.serialzer.


from django.db.models import QuerySet


class RemoteQueryset(GRPCConnection):
    def __init__(self, serializer, resource_type):
        self.serialzer = serializer
        self.resource_type = resource_type
        self._result_cache = None
        self.exclude_kwargs = {}
        self.filter_kwargs = {}
        self.order_args = []
        self.start_index = 0
        self.end_index = None

    # def __repr__(self):
    #     self._fetch_all()
    #     return str(self._result_cache)

    def __len__(self):
        self._fetch_all()
        return len(self._result_cache)

    def __iter__(self):
        self._fetch_all()
        return iter(self._result_cache)

    def __getitem__(self, k):
        pass

    def __bool__(self):
        pass

    def _get_query(self, action=Action.SELECT) -> Query:
        return Query(
            action=action,
            filter_kwargs=to_struct(self.filter_kwargs),
            exclude_kwargs=to_struct(self.exclude_kwargs),
            start_index=self.start_index,
            end_index=self.end_index,
            order=self.order_args,
            resource_type=self.resource_type,
        )

    def _fetch_all(self):
        if self._result_cache is None:
            self._result_cache = []
            for resp in self.single_request(self._get_query()):
                data = serializers.TestModelSerializer(data=MessageToDict(resp)["data"])
                data.is_valid()
                self._result_cache.append(RemoteObject(serializer=data))

    def filter(self, **kwargs):
        qs = self._chain()

        qs.filter_kwargs = {**self.filter_kwargs, **kwargs}
        return qs

    def exclude(self, **kwargs):
        qs = self._chain()
        qs.exclude_kwargs = {**self.exclude_kwargs, **kwargs}
        return qs

    def count(self):
        resp = next(self.single_request(self._get_query(action=Action.COUNT)))
        return int(resp.data["count"])

    def get(self, **kwargs) -> RemoteObject:
        self._fetch_all()
        assert len(self._result_cache) == 1
        return self._result_cache[0]

    def create(self, **kwargs) -> RemoteObject:
        self._result_cache = None
        resp = next(
            self.single_request(
                Query(
                    resource_type=self.resource_type,
                    action=Action.CREATE,
                    object_data=to_struct(kwargs),
                )
            )
        )
        data = serializers.TestModelSerializer(data=MessageToDict(resp)["data"])
        data.is_valid()
        return RemoteObject(serializer=data)

    def delete(self):
        self._result_cache = None
        next(self.single_request(self._get_query(action=Action.DELETE)))

    def update(self, **kwargs):
        self._result_cache = None
        query = self._get_query(action=Action.UPDATE)
        data = serializers.TestModelSerializer(
            data=MessageToDict(resp)["data"], partial=True
        )
        data.is_valid()
        query.object_data = to_struct(data.data)
        resp = next(self.single_request(query))

        return RemoteObject(serializer=data)

    def order_by(self, *args):
        qs = self._chain()
        qs.order_args = [*self.order_args, *args]
        return self

    def all(self):
        return self._chain()

    def _chain(self):

        return self._clone()

    def _clone(self):
        c = self.__class__(
            self.serialzer,
            self.resource_type,
        )
        return c
