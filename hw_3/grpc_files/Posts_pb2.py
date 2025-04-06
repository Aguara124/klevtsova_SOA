# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: grpc_files/Posts.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'grpc_files/Posts.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16grpc_files/Posts.proto\x12\x0esocial_network\"\x98\x01\n\x04Post\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05title\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x12\n\ncreator_id\x18\x04 \x01(\x05\x12\x15\n\rcreation_date\x18\x05 \x01(\t\x12\x13\n\x0bupdate_date\x18\x06 \x01(\t\x12\x12\n\nis_private\x18\x07 \x01(\x08\x12\x0c\n\x04tags\x18\x08 \x01(\t\"m\n\x11\x43reatePostRequest\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x12\n\ncreator_id\x18\x03 \x01(\x05\x12\x12\n\nis_private\x18\x04 \x01(\x08\x12\x0c\n\x04tags\x18\x05 \x01(\t\"6\n\x12\x43reatePostResponse\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\x12\x0f\n\x07message\x18\x02 \x01(\t\"j\n\x11UpdatePostRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\x12\r\n\x05title\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x12\n\nis_private\x18\x04 \x01(\x08\x12\x0c\n\x04tags\x18\x05 \x01(\t\"6\n\x12UpdatePostResponse\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\x12\x0f\n\x07message\x18\x02 \x01(\t\"$\n\x11\x44\x65letePostRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\"6\n\x12\x44\x65letePostResponse\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\x12\x0f\n\x07message\x18\x02 \x01(\t\"%\n\x12GetPostByIdRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\"9\n\x13GetPostByIdResponse\x12\"\n\x04post\x18\x01 \x01(\x0b\x32\x14.social_network.Post\"\x07\n\x05\x45mpty\";\n\x14GetPostsListResponse\x12#\n\x05posts\x18\x01 \x03(\x0b\x32\x14.social_network.Post2\xba\x03\n\x14SocialNetworkService\x12S\n\nCreatePost\x12!.social_network.CreatePostRequest\x1a\".social_network.CreatePostResponse\x12S\n\nUpdatePost\x12!.social_network.UpdatePostRequest\x1a\".social_network.UpdatePostResponse\x12S\n\nDeletePost\x12!.social_network.DeletePostRequest\x1a\".social_network.DeletePostResponse\x12V\n\x0bGetPostById\x12\".social_network.GetPostByIdRequest\x1a#.social_network.GetPostByIdResponse\x12K\n\x0cGetPostsList\x12\x15.social_network.Empty\x1a$.social_network.GetPostsListResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'grpc_files.Posts_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_POST']._serialized_start=43
  _globals['_POST']._serialized_end=195
  _globals['_CREATEPOSTREQUEST']._serialized_start=197
  _globals['_CREATEPOSTREQUEST']._serialized_end=306
  _globals['_CREATEPOSTRESPONSE']._serialized_start=308
  _globals['_CREATEPOSTRESPONSE']._serialized_end=362
  _globals['_UPDATEPOSTREQUEST']._serialized_start=364
  _globals['_UPDATEPOSTREQUEST']._serialized_end=470
  _globals['_UPDATEPOSTRESPONSE']._serialized_start=472
  _globals['_UPDATEPOSTRESPONSE']._serialized_end=526
  _globals['_DELETEPOSTREQUEST']._serialized_start=528
  _globals['_DELETEPOSTREQUEST']._serialized_end=564
  _globals['_DELETEPOSTRESPONSE']._serialized_start=566
  _globals['_DELETEPOSTRESPONSE']._serialized_end=620
  _globals['_GETPOSTBYIDREQUEST']._serialized_start=622
  _globals['_GETPOSTBYIDREQUEST']._serialized_end=659
  _globals['_GETPOSTBYIDRESPONSE']._serialized_start=661
  _globals['_GETPOSTBYIDRESPONSE']._serialized_end=718
  _globals['_EMPTY']._serialized_start=720
  _globals['_EMPTY']._serialized_end=727
  _globals['_GETPOSTSLISTRESPONSE']._serialized_start=729
  _globals['_GETPOSTSLISTRESPONSE']._serialized_end=788
  _globals['_SOCIALNETWORKSERVICE']._serialized_start=791
  _globals['_SOCIALNETWORKSERVICE']._serialized_end=1233
# @@protoc_insertion_point(module_scope)
