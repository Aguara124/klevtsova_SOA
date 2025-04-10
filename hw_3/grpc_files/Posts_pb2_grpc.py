# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from grpc_files import Posts_pb2 as grpc__files_dot_Posts__pb2

GRPC_GENERATED_VERSION = '1.71.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in grpc_files/Posts_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class SocialNetworkServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreatePost = channel.unary_unary(
                '/social_network.SocialNetworkService/CreatePost',
                request_serializer=grpc__files_dot_Posts__pb2.CreatePostRequest.SerializeToString,
                response_deserializer=grpc__files_dot_Posts__pb2.CreatePostResponse.FromString,
                _registered_method=True)
        self.UpdatePost = channel.unary_unary(
                '/social_network.SocialNetworkService/UpdatePost',
                request_serializer=grpc__files_dot_Posts__pb2.UpdatePostRequest.SerializeToString,
                response_deserializer=grpc__files_dot_Posts__pb2.UpdatePostResponse.FromString,
                _registered_method=True)
        self.DeletePost = channel.unary_unary(
                '/social_network.SocialNetworkService/DeletePost',
                request_serializer=grpc__files_dot_Posts__pb2.DeletePostRequest.SerializeToString,
                response_deserializer=grpc__files_dot_Posts__pb2.DeletePostResponse.FromString,
                _registered_method=True)
        self.GetPostById = channel.unary_unary(
                '/social_network.SocialNetworkService/GetPostById',
                request_serializer=grpc__files_dot_Posts__pb2.GetPostByIdRequest.SerializeToString,
                response_deserializer=grpc__files_dot_Posts__pb2.GetPostByIdResponse.FromString,
                _registered_method=True)
        self.GetPostsList = channel.unary_unary(
                '/social_network.SocialNetworkService/GetPostsList',
                request_serializer=grpc__files_dot_Posts__pb2.Empty.SerializeToString,
                response_deserializer=grpc__files_dot_Posts__pb2.GetPostsListResponse.FromString,
                _registered_method=True)


class SocialNetworkServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreatePost(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdatePost(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeletePost(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPostById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPostsList(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SocialNetworkServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreatePost': grpc.unary_unary_rpc_method_handler(
                    servicer.CreatePost,
                    request_deserializer=grpc__files_dot_Posts__pb2.CreatePostRequest.FromString,
                    response_serializer=grpc__files_dot_Posts__pb2.CreatePostResponse.SerializeToString,
            ),
            'UpdatePost': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdatePost,
                    request_deserializer=grpc__files_dot_Posts__pb2.UpdatePostRequest.FromString,
                    response_serializer=grpc__files_dot_Posts__pb2.UpdatePostResponse.SerializeToString,
            ),
            'DeletePost': grpc.unary_unary_rpc_method_handler(
                    servicer.DeletePost,
                    request_deserializer=grpc__files_dot_Posts__pb2.DeletePostRequest.FromString,
                    response_serializer=grpc__files_dot_Posts__pb2.DeletePostResponse.SerializeToString,
            ),
            'GetPostById': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPostById,
                    request_deserializer=grpc__files_dot_Posts__pb2.GetPostByIdRequest.FromString,
                    response_serializer=grpc__files_dot_Posts__pb2.GetPostByIdResponse.SerializeToString,
            ),
            'GetPostsList': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPostsList,
                    request_deserializer=grpc__files_dot_Posts__pb2.Empty.FromString,
                    response_serializer=grpc__files_dot_Posts__pb2.GetPostsListResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'social_network.SocialNetworkService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('social_network.SocialNetworkService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class SocialNetworkService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreatePost(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/social_network.SocialNetworkService/CreatePost',
            grpc__files_dot_Posts__pb2.CreatePostRequest.SerializeToString,
            grpc__files_dot_Posts__pb2.CreatePostResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdatePost(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/social_network.SocialNetworkService/UpdatePost',
            grpc__files_dot_Posts__pb2.UpdatePostRequest.SerializeToString,
            grpc__files_dot_Posts__pb2.UpdatePostResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeletePost(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/social_network.SocialNetworkService/DeletePost',
            grpc__files_dot_Posts__pb2.DeletePostRequest.SerializeToString,
            grpc__files_dot_Posts__pb2.DeletePostResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetPostById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/social_network.SocialNetworkService/GetPostById',
            grpc__files_dot_Posts__pb2.GetPostByIdRequest.SerializeToString,
            grpc__files_dot_Posts__pb2.GetPostByIdResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetPostsList(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/social_network.SocialNetworkService/GetPostsList',
            grpc__files_dot_Posts__pb2.Empty.SerializeToString,
            grpc__files_dot_Posts__pb2.GetPostsListResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
