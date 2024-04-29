import sys, os
import numpy as np # type: ignore
from typing import List

DO_VIZ = False


sys.path.append(os.path.join(os.path.dirname(__file__), "..", "tinygrad"))
from tinygrad import Tensor # type: ignore
from tinygrad.ops import LazyOp, BufferOps, LoadOps # type: ignore
from tinygrad.buffer import Buffer # type: ignore
from tinygrad.lazy import LazyBuffer # type: ignore
from tinygrad.features.graph import Inject # type: ignore
def visual_lazybuffer(lb:'LazyBuffer', scheduled=False, depth=0):
    global DO_VIZ
    if DO_VIZ:
        if lb.base.realized is None and lb.base.op is LoadOps.CONST: return
        if lb.base != lb:
            lb = lb.base
        if lb.realized is None:
            print("  "*depth + str(lb))
            for x in lb.srcs:
                visual_lazybuffer(x, scheduled, depth+1)
        else:
            print("  "*depth + f"(R) {lb}")
Inject.visual_lazybuffer = visual_lazybuffer


def get_contents(buf:Buffer) -> np.ndarray:
    return np.frombuffer(buf.as_buffer(allow_zero_copy=True), dtype=buf.dtype.np)

def parse_schedule(op:LazyOp, bufs:List[Buffer], depth:int=0):
    text = f"{op.op}"
    if op.op == BufferOps.LOAD:
        text += f" <shape {op.arg.st.shape}> <strided {tuple(a*b for a,b in zip(op.arg.st.shape, op.arg.st.real_strides()))}> <idx {op.arg.idx}>"
        print(get_contents(bufs[op.arg.idx]))
    print("  "*depth + text)
    for src in op.src:
        parse_schedule(src, bufs, depth+1)

if __name__ == "__main__":
    a = Tensor.arange(10).reshape(1,10)#.realize()
    b = Tensor.arange(5).reshape(5,1)  #.realize()

    c = a + b

    DO_VIZ = True
    c.realize()

    # schedule = c.schedule_with_vars()
    # for ei in schedule:
    #     for si in ei:
    #         print(si)
    #         print("Buffers:")
    #         for buf in si.bufs:
    #             print("  " + str(buf))
    #         for ast in si.ast:
    #             parse_schedule(ast, si.bufs)
