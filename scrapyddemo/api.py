import eventlet
# eventlet.monkey_patch()
from eventlet import Event
from eventlet import sleep

values = [1, 2, 3, 4, 5, 6]


def func(value):
    sleep(1)
    # print('pull value: %s'%value)
    return value


#
#
# def main():
#     results = []
#     pool = eventlet.GreenPool(3)
#
#     for value in values:
#         event = Event()
#         gt = pool.spawn(func, value)
#         gt.link(lambda res: event.send(res.wait()))
#         results.append(event)
#
#     # sleep(2)
#     for result in results:
#         if result.ready():
#             print(result.wait())
#         else:
#             print('waiting')

def handle_result(finished_thread, *args, **kwargs):
    print(finished_thread)
    args[0].send(finished_thread.wait())


def main():
    results = []
    pool = eventlet.GreenPool()

    for value in values:
        event = Event()
        gt = pool.spawn(func, value)
        # gt.link(handle_result,event)
        gt.link(lambda res: event.send(res.wait()))
        results.append(event)

    for result in results:
        if result.ready():
            print('result: %s' % result.wait())
        else:
            print('waiting')


if __name__ == '__main__':
    main()
