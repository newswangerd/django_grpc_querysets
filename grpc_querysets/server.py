from grpc_querysets.lib.query_pb2 import Query, Action, Response
from grpc_querysets.lib.query_pb2_grpc import RemoteQuerysetServicer
from rest_framework.serializers import ModelSerializer
import traceback
from google.protobuf.json_format import MessageToJson, MessageToDict
from google.protobuf.struct_pb2 import Struct


def to_struct(data: dict) -> Struct:
    s = Struct()
    s.update(data)
    return s


class QueryServer(RemoteQuerysetServicer):
    def __init__(self, serializers) -> None:
        self.serialzers = serializers
        super().__init__()

    def SingleQuery(self, request: Query, context):
        try:
            print("received request")
            print(MessageToJson(request))
            serializer: ModelSerializer = self.serialzers[request.resource_type]
            model = serializer.Meta.model

            if request.action in (
                Action.SELECT,
                Action.DELETE,
                Action.COUNT,
                Action.UPDATE,
            ):

                qs = model.objects.all()
                if filter := request.filter_kwargs:
                    qs = qs.filter(**filter)
                if exclude := request.exclude_kwargs:
                    qs = qs.exclude(**exclude)

                qs = qs.order_by(*request.order)

                if request.action == Action.SELECT:
                    end_index = None
                    if request.end_index != 0:
                        end_index = request.end_index
                    for obj in qs[request.start_index : end_index]:
                        yield Response(
                            action=request.action, data=to_struct(serializer(obj).data)
                        )
                elif request.action == Action.DELETE:
                    qs.delete()
                    yield Response(action=request.action, data={})
                elif request.action == Action.COUNT:
                    yield Response(
                        action=request.action,
                        data=to_struct(
                            {"count": qs.count()},
                        ),
                    )
                elif request.action == Action.UPDATE:
                    data = serializer(data=MessageToDict(request.object_data))
                    data.is_valid(raise_exception=True)
                    qs.update(**data)
                    yield Response(action=request.action)

            elif request.action == Action.CREATE:
                data = serializer(data=MessageToDict(request.object_data))
                data.is_valid(raise_exception=True)
                obj = model.objects.create(**data.validated_data)

                yield Response(
                    action=request.action,
                    data=to_struct(serializer(obj).data),
                )

        except Exception as e:
            print(e)
            traceback.print_exc()
            raise

    # def TransactionalQuery(self, request_iterator, context):
    #     return super().TransactionalQuery(request_iterator, context)
