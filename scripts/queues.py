# %%
import sys
sys.path.append('./')

from plasma.parallel_processing import queues

# %%
def test(x):
    return f'{x:05d}'

# %%
q = (
    queues.ThreadQueue(n=5)\
    .register_callback(test)\
    .chain(print)\
    .run()
)

# %%
for i in range(20):
    q.put(i)

# %%
q.put(queues.Signal.IGNORE)

# %%
q.release()


def test_process(x):
    print(x + 5)


if __name__ == '__main__':
    # %%
    array = []
    q = (
        queues.ProcessQueue(qsize=5)
        .register_callback(test_process)
        # .on_exception(lambda d, e: array.append(f'{d} - {type(e)}'))
        .chain(print)
        .run()
    )
    for i in range(10):
        q.put(i)
    q.release()
