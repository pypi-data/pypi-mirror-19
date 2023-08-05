"""Python wrappers around Brain.

This file is MACHINE GENERATED! Do not edit.
"""

import collections

from google.protobuf import text_format

from tensorflow.core.framework import op_def_pb2

# Needed to trigger the call to _set_call_cpp_shape_fn.
from tensorflow.python.framework import common_shapes

from tensorflow.python.framework import op_def_registry
from tensorflow.python.framework import ops
from tensorflow.python.framework import op_def_library
__fact_outputs = ["fact"]


def _fact(name=None):
  r"""Output a fact about factorials.

  Args:
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `string`.
  """
  result = _op_def_lib.apply_op("Fact", name=name)
  return result


def _InitOpDefLibrary():
  op_list = op_def_pb2.OpList()
  text_format.Merge(_InitOpDefLibrary.op_list_ascii, op_list)
  op_def_registry.register_op_list(op_list)
  op_def_lib = op_def_library.OpDefLibrary()
  op_def_lib.add_op_list(op_list)
  return op_def_lib


_InitOpDefLibrary.op_list_ascii = """op {
  name: "Fact"
  output_arg {
    name: "fact"
    type: DT_STRING
  }
}
"""


_op_def_lib = _InitOpDefLibrary()
