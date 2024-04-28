import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "tinygrad"))
from tinygrad import Tensor
from tinygrad.ops import LazyOp, BufferOps

def parse_schedule(op:LazyOp, depth:int=0):
    text = f"{op.op}"
    if op.op == BufferOps.LOAD:
        text += f" <shape={op.arg.st.shape}>"
    print("  "*depth + text)
    for src in op.src:
        parse_schedule(src, depth+1)

if __name__ == "__main__":
    a = Tensor.arange(10).reshape(1,10).realize()
    b = Tensor.arange(5).reshape(5,1).realize()

    c = a + b

    schedule = c.schedule_with_vars()
    for entry in schedule:
        for item in entry:
            for ast in item.ast:
                parse_schedule(ast)
