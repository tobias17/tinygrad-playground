import sys, os
import numpy as np # type: ignore
from typing import List, Set


sys.path.append(os.path.join(os.path.dirname(__file__), "..", "tinygrad"))
from tinygrad import Tensor # type: ignore
from tinygrad.ops import LazyOp, BufferOps, LoadOps # type: ignore
from tinygrad.buffer import Buffer # type: ignore
from tinygrad.lazy import LazyBuffer # type: ignore
from tinygrad.features.graph import Inject # type: ignore

DO_VIZ = False
seen: Set[LazyBuffer] = set()
def visual_lazybuffer(lb:'LazyBuffer', scheduled=False, depth=0):
    global DO_VIZ, seen
    if DO_VIZ:
        if lb in seen:
            return
        seen.add(lb)
        print("  "*depth + str(lb))
        if hasattr(lb, "srcs"):
            for src in lb.srcs:
                visual_lazybuffer(src, depth=depth+1)
        elif lb != lb.base:
            visual_lazybuffer(lb.base, depth=depth+1)
Inject.visual_lazybuffer = visual_lazybuffer


def get_contents(buf:Buffer) -> np.ndarray:
    return np.frombuffer(buf.as_buffer(allow_zero_copy=True), dtype=buf.dtype.np)

def parse_schedule(op:LazyOp, bufs:List[Buffer], depth:int=0):
    text = f"{op.op}"
    if op.op == BufferOps.LOAD:
        print(get_contents(bufs[op.arg.idx]))
        if any(v is None for v in op.arg.st.real_strides()):
            print("  "*depth + f"Before: {op.arg.st.real_strides()}")
            op.arg.st.simplify()
            print("  "*depth + f"After:  {op.arg.st.real_strides()}")
        text += f" <shape {op.arg.st.shape}> <strides {op.arg.st.real_strides()}> <idx {op.arg.idx}> <exp {op.arg.st.expr_idxs()}>"
    print("  "*depth + text)
    for src in op.src:
        parse_schedule(src, bufs, depth+1)

if __name__ == "__main__":
    a = Tensor.arange(10).reshape(1,10)
    b = Tensor.arange(5).reshape(5,1).expand(5,2).reshape(1,10)

    c = a + b

    DO_VIZ = True
    c.realize()

    # schedule = c.schedule_with_vars()
    # for ei in schedule:
    #     for si in ei:
    #         # print(si)
    #         print("Buffers:")
    #         for buf in si.bufs:
    #             print("  " + str(buf))
    #         for ast in si.ast:
    #             parse_schedule(ast, si.bufs)
