# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: frame.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='frame.proto',
  package='frames',
  syntax='proto3',
  serialized_pb=_b('\n\x0b\x66rame.proto\x12\x06\x66rames\"\x8d\x01\n\x0c\x46rameMessage\x12\x15\n\rprocessing_id\x18\x01 \x01(\t\x12)\n\x05\x66rame\x18\x02 \x01(\x0b\x32\x1a.frames.FrameMessage.Frame\x1a;\n\x05\x46rame\x12\x14\n\x0c\x66rame_number\x18\x01 \x01(\x05\x12\r\n\x05shape\x18\x02 \x03(\x05\x12\r\n\x05\x66rame\x18\x03 \x01(\x0c\x62\x06proto3')
)




_FRAMEMESSAGE_FRAME = _descriptor.Descriptor(
  name='Frame',
  full_name='frames.FrameMessage.Frame',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='frame_number', full_name='frames.FrameMessage.Frame.frame_number', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='shape', full_name='frames.FrameMessage.Frame.shape', index=1,
      number=2, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='frame', full_name='frames.FrameMessage.Frame.frame', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=106,
  serialized_end=165,
)

_FRAMEMESSAGE = _descriptor.Descriptor(
  name='FrameMessage',
  full_name='frames.FrameMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='processing_id', full_name='frames.FrameMessage.processing_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='frame', full_name='frames.FrameMessage.frame', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_FRAMEMESSAGE_FRAME, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=24,
  serialized_end=165,
)

_FRAMEMESSAGE_FRAME.containing_type = _FRAMEMESSAGE
_FRAMEMESSAGE.fields_by_name['frame'].message_type = _FRAMEMESSAGE_FRAME
DESCRIPTOR.message_types_by_name['FrameMessage'] = _FRAMEMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FrameMessage = _reflection.GeneratedProtocolMessageType('FrameMessage', (_message.Message,), dict(

  Frame = _reflection.GeneratedProtocolMessageType('Frame', (_message.Message,), dict(
    DESCRIPTOR = _FRAMEMESSAGE_FRAME,
    __module__ = 'frame_pb2'
    # @@protoc_insertion_point(class_scope:frames.FrameMessage.Frame)
    ))
  ,
  DESCRIPTOR = _FRAMEMESSAGE,
  __module__ = 'frame_pb2'
  # @@protoc_insertion_point(class_scope:frames.FrameMessage)
  ))
_sym_db.RegisterMessage(FrameMessage)
_sym_db.RegisterMessage(FrameMessage.Frame)


# @@protoc_insertion_point(module_scope)