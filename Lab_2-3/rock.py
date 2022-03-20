import threading
import time

temp = 0
locker = threading.Lock()

def method(data: str, potok):
    global temp
    while True:
        locker.acquire()
        temp += 1
        print(f"{temp}   thread - {potok}")
        time.sleep(0.1)
        locker.release()

list_of_threads = []

for i in range(3):
    thr = threading.Thread(target=method, args=("12333", i), name=f"thread-{i}")
    list_of_threads.append(thr)
    thr.start()

# for i in list_of_threads:
#     i.join()


#
# def jopa(rock: str, count_iteration: int, current_thread):
#     for i in range(count_iteration):
#         rock += ("" + rock)
#     print(f'string: {rock},\n count_iteration: {count_iteration},\n current_thread: {current_thread}\n')
#     time.sleep(1)
#
# list_of_thread = []
#
# for i in range(3):
#     thr = threading.Thread(target=jopa, args=('', random.randint(1, 20), i), name=f'thr-{i}')
#     list_of_thread.append(thr)
#     thr.start()
#
# for i in list_of_thread:
#     i.join()
# print(list_of_thread)