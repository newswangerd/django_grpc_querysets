protobuf:
	python -m grpc_tools.protoc \
	-I ${PWD} \
	--python_out=${PWD} \
	--pyi_out=${PWD} \
	--grpc_python_out=${PWD} \
	${PWD}/grpc_querysets/lib/query.proto