import grpc
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities

import properform_pb2 as properform__pb2
import properform_pb2 as properform__pb2


class ProperformStub(object):

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Push = channel.unary_unary(
        '/properform.Properform/Push',
        request_serializer=properform__pb2.Profile.SerializeToString,
        response_deserializer=properform__pb2.PushReply.FromString,
        )


class ProperformServicer(object):

  def Push(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ProperformServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Push': grpc.unary_unary_rpc_method_handler(
          servicer.Push,
          request_deserializer=properform__pb2.Profile.FromString,
          response_serializer=properform__pb2.PushReply.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'properform.Properform', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
