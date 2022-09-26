# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: frames.proto

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
  name='frames.proto',
  package='frames',
  syntax='proto3',
  serialized_pb=_b('\n\x0c\x66rames.proto\x12\x06\x66rames\"\x8d\x01\n\x0c\x46rameMessage\x12\x15\n\rprocessing_id\x18\x01 \x01(\t\x12)\n\x05\x66rame\x18\x02 \x01(\x0b\x32\x1a.frames.FrameMessage.Frame\x1a;\n\x05\x46rame\x12\x14\n\x0c\x66rame_number\x18\x01 \x01(\x05\x12\r\n\x05shape\x18\x02 \x03(\x05\x12\r\n\x05\x66rame\x18\x03 \x01(\x0c\"\xeb\x01\n\nMotorcycle\x12\x15\n\rprocessing_id\x18\x01 \x01(\t\x12\x15\n\rmotorcycle_id\x18\x02 \x01(\t\x12\'\n\x05\x66rame\x18\x03 \x01(\x0b\x32\x18.frames.Motorcycle.Frame\x12%\n\x04\x62\x62ox\x18\x04 \x01(\x0b\x32\x17.frames.Motorcycle.BBox\x1a;\n\x05\x46rame\x12\x14\n\x0c\x66rame_number\x18\x01 \x01(\x05\x12\r\n\x05shape\x18\x02 \x03(\x05\x12\r\n\x05\x66rame\x18\x03 \x01(\x0c\x1a\"\n\x04\x42\x42ox\x12\r\n\x05shape\x18\x01 \x03(\x05\x12\x0b\n\x03\x62ox\x18\x02 \x01(\x0c\"\xe6\x01\n\x05Plate\x12\x15\n\rprocessing_id\x18\x01 \x01(\t\x12\x10\n\x08plate_id\x18\x02 \x01(\t\x12\"\n\x05\x66rame\x18\x03 \x01(\x0b\x32\x13.frames.Plate.Frame\x12 \n\x04\x62\x62ox\x18\x04 \x01(\x0b\x32\x12.frames.Plate.BBox\x1a;\n\x05\x46rame\x12\x14\n\x0c\x66rame_number\x18\x01 \x01(\x05\x12\r\n\x05shape\x18\x02 \x03(\x05\x12\r\n\x05\x66rame\x18\x03 \x01(\x0c\x1a\x31\n\x04\x42\x42ox\x12\r\n\x05shape\x18\x01 \x03(\x05\x12\x0b\n\x03\x62ox\x18\x02 \x01(\x0c\x12\r\n\x05label\x18\x03 \x01(\t\"\xf7\x01\n\tPlateText\x12\x15\n\rprocessing_id\x18\x01 \x01(\t\x12\x10\n\x08plate_id\x18\x02 \x01(\t\x12&\n\x05\x66rame\x18\x03 \x01(\x0b\x32\x17.frames.PlateText.Frame\x12$\n\x04\x62\x62ox\x18\x04 \x01(\x0b\x32\x16.frames.PlateText.BBox\x12\x12\n\nplate_text\x18\x05 \x01(\t\x1a;\n\x05\x46rame\x12\x14\n\x0c\x66rame_number\x18\x01 \x01(\x05\x12\r\n\x05shape\x18\x02 \x03(\x05\x12\r\n\x05\x66rame\x18\x03 \x01(\x0c\x1a\"\n\x04\x42\x42ox\x12\r\n\x05shape\x18\x01 \x03(\x05\x12\x0b\n\x03\x62ox\x18\x02 \x01(\x0c\x62\x06proto3')
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
  serialized_start=107,
  serialized_end=166,
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
  serialized_start=25,
  serialized_end=166,
)


_MOTORCYCLE_FRAME = _descriptor.Descriptor(
  name='Frame',
  full_name='frames.Motorcycle.Frame',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='frame_number', full_name='frames.Motorcycle.Frame.frame_number', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='shape', full_name='frames.Motorcycle.Frame.shape', index=1,
      number=2, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='frame', full_name='frames.Motorcycle.Frame.frame', index=2,
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
  serialized_start=107,
  serialized_end=166,
)

_MOTORCYCLE_BBOX = _descriptor.Descriptor(
  name='BBox',
  full_name='frames.Motorcycle.BBox',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='shape', full_name='frames.Motorcycle.BBox.shape', index=0,
      number=1, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='box', full_name='frames.Motorcycle.BBox.box', index=1,
      number=2, type=12, cpp_type=9, label=1,
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
  serialized_start=370,
  serialized_end=404,
)

_MOTORCYCLE = _descriptor.Descriptor(
  name='Motorcycle',
  full_name='frames.Motorcycle',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='processing_id', full_name='frames.Motorcycle.processing_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='motorcycle_id', full_name='frames.Motorcycle.motorcycle_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='frame', full_name='frames.Motorcycle.frame', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bbox', full_name='frames.Motorcycle.bbox', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_MOTORCYCLE_FRAME, _MOTORCYCLE_BBOX, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=169,
  serialized_end=404,
)


_PLATE_FRAME = _descriptor.Descriptor(
  name='Frame',
  full_name='frames.Plate.Frame',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='frame_number', full_name='frames.Plate.Frame.frame_number', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='shape', full_name='frames.Plate.Frame.shape', index=1,
      number=2, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='frame', full_name='frames.Plate.Frame.frame', index=2,
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
  serialized_start=107,
  serialized_end=166,
)

_PLATE_BBOX = _descriptor.Descriptor(
  name='BBox',
  full_name='frames.Plate.BBox',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='shape', full_name='frames.Plate.BBox.shape', index=0,
      number=1, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='box', full_name='frames.Plate.BBox.box', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='label', full_name='frames.Plate.BBox.label', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=588,
  serialized_end=637,
)

_PLATE = _descriptor.Descriptor(
  name='Plate',
  full_name='frames.Plate',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='processing_id', full_name='frames.Plate.processing_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='plate_id', full_name='frames.Plate.plate_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='frame', full_name='frames.Plate.frame', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bbox', full_name='frames.Plate.bbox', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_PLATE_FRAME, _PLATE_BBOX, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=407,
  serialized_end=637,
)


_PLATETEXT_FRAME = _descriptor.Descriptor(
  name='Frame',
  full_name='frames.PlateText.Frame',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='frame_number', full_name='frames.PlateText.Frame.frame_number', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='shape', full_name='frames.PlateText.Frame.shape', index=1,
      number=2, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='frame', full_name='frames.PlateText.Frame.frame', index=2,
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
  serialized_start=107,
  serialized_end=166,
)

_PLATETEXT_BBOX = _descriptor.Descriptor(
  name='BBox',
  full_name='frames.PlateText.BBox',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='shape', full_name='frames.PlateText.BBox.shape', index=0,
      number=1, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='box', full_name='frames.PlateText.BBox.box', index=1,
      number=2, type=12, cpp_type=9, label=1,
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
  serialized_start=370,
  serialized_end=404,
)

_PLATETEXT = _descriptor.Descriptor(
  name='PlateText',
  full_name='frames.PlateText',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='processing_id', full_name='frames.PlateText.processing_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='plate_id', full_name='frames.PlateText.plate_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='frame', full_name='frames.PlateText.frame', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bbox', full_name='frames.PlateText.bbox', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='plate_text', full_name='frames.PlateText.plate_text', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_PLATETEXT_FRAME, _PLATETEXT_BBOX, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=640,
  serialized_end=887,
)

_FRAMEMESSAGE_FRAME.containing_type = _FRAMEMESSAGE
_FRAMEMESSAGE.fields_by_name['frame'].message_type = _FRAMEMESSAGE_FRAME
_MOTORCYCLE_FRAME.containing_type = _MOTORCYCLE
_MOTORCYCLE_BBOX.containing_type = _MOTORCYCLE
_MOTORCYCLE.fields_by_name['frame'].message_type = _MOTORCYCLE_FRAME
_MOTORCYCLE.fields_by_name['bbox'].message_type = _MOTORCYCLE_BBOX
_PLATE_FRAME.containing_type = _PLATE
_PLATE_BBOX.containing_type = _PLATE
_PLATE.fields_by_name['frame'].message_type = _PLATE_FRAME
_PLATE.fields_by_name['bbox'].message_type = _PLATE_BBOX
_PLATETEXT_FRAME.containing_type = _PLATETEXT
_PLATETEXT_BBOX.containing_type = _PLATETEXT
_PLATETEXT.fields_by_name['frame'].message_type = _PLATETEXT_FRAME
_PLATETEXT.fields_by_name['bbox'].message_type = _PLATETEXT_BBOX
DESCRIPTOR.message_types_by_name['FrameMessage'] = _FRAMEMESSAGE
DESCRIPTOR.message_types_by_name['Motorcycle'] = _MOTORCYCLE
DESCRIPTOR.message_types_by_name['Plate'] = _PLATE
DESCRIPTOR.message_types_by_name['PlateText'] = _PLATETEXT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FrameMessage = _reflection.GeneratedProtocolMessageType('FrameMessage', (_message.Message,), dict(

  Frame = _reflection.GeneratedProtocolMessageType('Frame', (_message.Message,), dict(
    DESCRIPTOR = _FRAMEMESSAGE_FRAME,
    __module__ = 'frames_pb2'
    # @@protoc_insertion_point(class_scope:frames.FrameMessage.Frame)
    ))
  ,
  DESCRIPTOR = _FRAMEMESSAGE,
  __module__ = 'frames_pb2'
  # @@protoc_insertion_point(class_scope:frames.FrameMessage)
  ))
_sym_db.RegisterMessage(FrameMessage)
_sym_db.RegisterMessage(FrameMessage.Frame)

Motorcycle = _reflection.GeneratedProtocolMessageType('Motorcycle', (_message.Message,), dict(

  Frame = _reflection.GeneratedProtocolMessageType('Frame', (_message.Message,), dict(
    DESCRIPTOR = _MOTORCYCLE_FRAME,
    __module__ = 'frames_pb2'
    # @@protoc_insertion_point(class_scope:frames.Motorcycle.Frame)
    ))
  ,

  BBox = _reflection.GeneratedProtocolMessageType('BBox', (_message.Message,), dict(
    DESCRIPTOR = _MOTORCYCLE_BBOX,
    __module__ = 'frames_pb2'
    # @@protoc_insertion_point(class_scope:frames.Motorcycle.BBox)
    ))
  ,
  DESCRIPTOR = _MOTORCYCLE,
  __module__ = 'frames_pb2'
  # @@protoc_insertion_point(class_scope:frames.Motorcycle)
  ))
_sym_db.RegisterMessage(Motorcycle)
_sym_db.RegisterMessage(Motorcycle.Frame)
_sym_db.RegisterMessage(Motorcycle.BBox)

Plate = _reflection.GeneratedProtocolMessageType('Plate', (_message.Message,), dict(

  Frame = _reflection.GeneratedProtocolMessageType('Frame', (_message.Message,), dict(
    DESCRIPTOR = _PLATE_FRAME,
    __module__ = 'frames_pb2'
    # @@protoc_insertion_point(class_scope:frames.Plate.Frame)
    ))
  ,

  BBox = _reflection.GeneratedProtocolMessageType('BBox', (_message.Message,), dict(
    DESCRIPTOR = _PLATE_BBOX,
    __module__ = 'frames_pb2'
    # @@protoc_insertion_point(class_scope:frames.Plate.BBox)
    ))
  ,
  DESCRIPTOR = _PLATE,
  __module__ = 'frames_pb2'
  # @@protoc_insertion_point(class_scope:frames.Plate)
  ))
_sym_db.RegisterMessage(Plate)
_sym_db.RegisterMessage(Plate.Frame)
_sym_db.RegisterMessage(Plate.BBox)

PlateText = _reflection.GeneratedProtocolMessageType('PlateText', (_message.Message,), dict(

  Frame = _reflection.GeneratedProtocolMessageType('Frame', (_message.Message,), dict(
    DESCRIPTOR = _PLATETEXT_FRAME,
    __module__ = 'frames_pb2'
    # @@protoc_insertion_point(class_scope:frames.PlateText.Frame)
    ))
  ,

  BBox = _reflection.GeneratedProtocolMessageType('BBox', (_message.Message,), dict(
    DESCRIPTOR = _PLATETEXT_BBOX,
    __module__ = 'frames_pb2'
    # @@protoc_insertion_point(class_scope:frames.PlateText.BBox)
    ))
  ,
  DESCRIPTOR = _PLATETEXT,
  __module__ = 'frames_pb2'
  # @@protoc_insertion_point(class_scope:frames.PlateText)
  ))
_sym_db.RegisterMessage(PlateText)
_sym_db.RegisterMessage(PlateText.Frame)
_sym_db.RegisterMessage(PlateText.BBox)


# @@protoc_insertion_point(module_scope)
