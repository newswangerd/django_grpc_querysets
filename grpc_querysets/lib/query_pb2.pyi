from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Action(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NONE: _ClassVar[Action]
    SELECT: _ClassVar[Action]
    CREATE: _ClassVar[Action]
    DELETE: _ClassVar[Action]
    UPDATE: _ClassVar[Action]
    COUNT: _ClassVar[Action]
NONE: Action
SELECT: Action
CREATE: Action
DELETE: Action
UPDATE: Action
COUNT: Action

class Query(_message.Message):
    __slots__ = ("action", "filter_kwargs", "exclude_kwargs", "start_index", "end_index", "order", "object_data", "resource_type")
    ACTION_FIELD_NUMBER: _ClassVar[int]
    FILTER_KWARGS_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_KWARGS_FIELD_NUMBER: _ClassVar[int]
    START_INDEX_FIELD_NUMBER: _ClassVar[int]
    END_INDEX_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    OBJECT_DATA_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    action: Action
    filter_kwargs: _struct_pb2.Struct
    exclude_kwargs: _struct_pb2.Struct
    start_index: int
    end_index: int
    order: _containers.RepeatedScalarFieldContainer[str]
    object_data: _struct_pb2.Struct
    resource_type: str
    def __init__(self, action: _Optional[_Union[Action, str]] = ..., filter_kwargs: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., exclude_kwargs: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., start_index: _Optional[int] = ..., end_index: _Optional[int] = ..., order: _Optional[_Iterable[str]] = ..., object_data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., resource_type: _Optional[str] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("action", "data")
    ACTION_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    action: Action
    data: _struct_pb2.Struct
    def __init__(self, action: _Optional[_Union[Action, str]] = ..., data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
