"""
Протокол ARQ.
1)-------------- SAW - Stop and wait -------------------------------
Между отправителем А и получателем В существует прямой канал связи и обратный.
На обеих сторонах производится обнаружение ошибок в пакетах.
Отправитель, после передачи пакета получателю, останавливается и ожидает реакции.
Реакция - true, если пакет передан без потерь и ошибок, false, если ошибки есть.
Сущетсвует определенное время ожидания - timeout. Если реакции не последовало, то отправитель по истечению определенного задаваемого времени
принимает решение о том, что пакет пришел поврежденным и отправляет его еще раз.

2)
3)
"""

import random
import time
from termcolor import colored, cprint
import networkx as nx
list_sender = []
list_receiver = []
queue_sender = []
queue_receiver = []

graph = nx.Graph()

graph.add_node('sender', qs=queue_sender, ls = list_sender)
graph.add_node('receiver', qr=queue_receiver, lr = list_receiver)


def check_errors(package: list):  # возвращает 1, если ошибок в пакете нет
    if "~" not in package:
        return 1
    else:
        return 0


def generate_package():
    return [str(random.randint(0, 999999999999999))]


# ARQ types
def stop_and_wait():
    question = int(input(colored("Количество пакетов: ", "white")))
    for i in range(question):
        queue_sender.append(generate_package())
    start = time.perf_counter()

    for i in range(len(queue_sender)):
        temp = random.randint(0, 10)
        if temp == 7:
            queue_sender[i].append("~")

    for i in range(len(queue_sender)):
        current_package = queue_sender[i]
        print(colored(f"Отправитель: {i}-й пакет отправлен ", 'blue'))
        time.sleep(0.5)
        queue_receiver.append(current_package)
        if "~" not in current_package:
            answer_receiver = 1
        else:
            answer_receiver = 0
        list_sender.append(answer_receiver)

        if answer_receiver == 1:
            print(colored(f"Получатель: {i} - й пакет принят без ошибок!", "green"))
        else:
            print(colored(f"Получатель: ########### {i}-й пакет принят с ошибкой ###########", "red"))
            queue_sender[i].remove("~")
            print(colored(f"Отправитель: ------------- {i}-й пакет отправлен повторно -------------", "blue"))
            time.sleep(0.5)
            queue_receiver.append(current_package)
            if "~" not in current_package:
                answer_receiver = 1
            else:
                answer_receiver = 0
            list_sender.append(answer_receiver)
            if answer_receiver == 1:
                print(colored(f"Получатель:{i} - й пакет принят без ошибок!", "green"))
            else:
                print(colored(f"Получатель: ################ {i}-й пакет принят с ошибкой ################", "red"))
    stop = time.perf_counter()
    print(colored(f"Время работы: {stop - start}", "yellow", attrs=['underline']))


def selective_repeat():
    question = int(input(colored("Количество пакетов: ", "white")))
    start = time.perf_counter()
    for i in range(question):
        queue_sender.append(generate_package())

    for i in range(len(queue_sender)):
        temp = random.randint(0, 10)
        if temp == 7:
            queue_sender[i].append("~")
            queue_sender[i].append(i)
        else:
            queue_sender[i].append(i)
    i = 0
    while True:
        current_package = queue_sender[i]
        queue_receiver.append(current_package)
        print(colored(f"Отправитель: {i}-й пакет отправлен ", 'blue'))
        queue_receiver.append(queue_sender[i+1])
        print(colored(f"Отправитель: {i+1}-й пакет отправлен ", 'blue'))
        queue_receiver.append(queue_sender[i + 2])
        print(colored(f"Отправитель: {i+2}-й пакет отправлен ", 'blue'))
        time.sleep(0.5)
        answer_receiver_1 = check_errors(current_package)
        answer_receiver_2 = check_errors(queue_sender[i+1])
        answer_receiver_3 = check_errors(queue_sender[i+2])
        if answer_receiver_1 == 1 and answer_receiver_2 == 1 and answer_receiver_3 == 1:
            print(colored(f"    Получатель: {i}-й пакет получен без ошибок ", 'green'))
            print(colored(f"    Получатель: {i+1}-й пакет получен без ошибок ", 'green'))
            print(colored(f"    Получатель: {i+2}-й пакет получен без ошибок ", 'green'))
            list_receiver.append(i)
            list_receiver.append(i+1)
            list_receiver.append(i+2)
            print(colored(f"Полученные пакеты: {list_receiver}", "white"))
            i += 3
            if i >= len(queue_sender) - 1:
                break
            else:
                continue
        else:
            if answer_receiver_1 == 0:
                print(colored(f"    Получатель: ######### {i}-й пакет получен с ошибкой #########", 'red'))
                print(colored(f"    Получатель: {i + 1}-й пакет получен без ошибок ", 'green'))
                print(colored(f"    Получатель: {i + 2}-й пакет получен без ошибок ", 'green'))
                current_package = queue_sender[i]
                current_package.remove("~")
                queue_receiver.append(current_package)
                print(colored(f"------------Отправитель: {i}-й пакет отправлен повторно ------------ ", 'blue'))
                print(colored(f"    Получатель: {i}-й пакет получен без ошибок ", 'green'))
                list_receiver.append(i)
                list_receiver.append(i+1)
                list_receiver.append(i+2)
                print(colored(f"Полученные пакеты: {list_receiver}", "white"))
                i += 3
                if i >= len(queue_sender) - 1:
                    break
                else:
                    continue

            if answer_receiver_2 == 0:
                print(colored(f"    Получатель: {i}-й пакет получен без ошибок ", 'green'))
                print(colored(f"    Получатель: ######### {i+1}-й пакет получен с ошибкой #########", 'red'))
                print(colored(f"    Получатель: {i + 2}-й пакет получен без ошибок ", 'green'))
                current_package = queue_sender[i+1]
                current_package.remove("~")
                queue_receiver.append(current_package)
                print(colored(f"------------Отправитель: {i+1}-й пакет отправлен повторно ------------ ", 'blue'))
                print(colored(f"    Получатель: {i+1}-й пакет получен без ошибок ", 'green'))
                list_receiver.append(i+1)
                list_receiver.append(i)
                list_receiver.append(i + 2)
                print(colored(f"Полученные пакеты: {list_receiver}", "white"))
                i += 3
                if i >= len(queue_sender) - 1:
                    break
                else:
                    continue
            if answer_receiver_3 == 0:
                print(colored(f"    Получатель: {i}-й пакет получен без ошибок ", 'green'))
                print(colored(f"    Получатель: {i + 1}-й пакет получен без ошибок ", 'green'))
                print(colored(f"    Получатель: ######### {i+2}-й пакет получен с ошибкой #########", 'red'))
                current_package = queue_sender[i+2]
                current_package.remove("~")
                queue_receiver.append(current_package)
                print(colored(f"------------Отправитель: {i+2}-й пакет отправлен повторно ------------ ", 'blue'))
                print(colored(f"    Получатель: {i+2}-й пакет получен без ошибок ", 'green'))
                list_receiver.append(i+2)
                list_receiver.append(i + 1)
                list_receiver.append(i)
                print(colored(f"Полученные пакеты: {list_receiver}", "white"))
                i += 3
                if i >= len(queue_sender) - 1:
                    break
                else:
                    continue
        if i >= len(queue_sender) - 1:
            break
    stop = time.perf_counter()
    print(sorted(list_receiver))
    print(colored(f"Время работы: {(stop - start)}", "yellow", attrs=['underline']))







def go_back_n():
    size_frame = 3
    question = int(input(colored("Количество пакетов: ", "white")))
    start = time.perf_counter()
    for i in range(question):
        queue_sender.append(generate_package())

    for i in range(len(queue_sender)):
        temp = random.randint(0, 10)
        if temp == 7:
            queue_sender[i].append("~")
            queue_sender[i].append(i)
        else:
            queue_sender[i].append(i)

    i = 0
    while True:
        current_package_1 = queue_sender[i]
        current_package_2 = queue_sender[i+1]
        current_package_3 = queue_sender[i+2]
        queue_receiver.append(current_package_1)
        queue_receiver.append(current_package_2)
        queue_receiver.append(current_package_3)
        print(colored(f"Отправитель: Пакеты {i}, {i+1}, {i+2} были отправлены", "blue"))
        time.sleep(0.6)
        if ("~" not in current_package_1) and ("~" not in current_package_2) and ("~" not in current_package_3):
            answer_receiver = True
        else:
            answer_receiver = False
        list_sender.append(answer_receiver)
        if answer_receiver is True:
            print(colored(f"    Получатель: Пакеты {i}, {i+1}, {i+2} были приняты без ошибок", "green"))
        else:
            print(colored(f"    Получатель: ################ Пакеты {i}, {i+1}, {i+2} приняты с ошибкой ################", "red"))
            check = None
            if "~" in current_package_1:
                check = 1
            if "~" in current_package_2:
                check = 2
            if "~" in current_package_3:
                check = 3
            match check:
                case 1:
                    current_package_1.remove("~")
                    try:
                        current_package_2.remove("~")
                        current_package_3.remove("~")
                    except:
                        pass
                    print(colored(f"------------- Отправитель: Пакеты {i}, {i + 1}, {i + 2} были отправлены повторно -------------", "blue"))
                    time.sleep(0.6)
                    queue_receiver.append(current_package_1)
                    queue_receiver.append(current_package_2)
                    queue_receiver.append(current_package_3)
                    print(colored(f"    Получатель: Пакеты {i}, {i+1}, {i+2} были приняты без ошибок", "green"))
                case 2:
                    current_package_2.remove("~")
                    try:
                        current_package_3.remove("~")
                    except:
                        pass
                    print(colored(
                        f"------------- Отправитель: Пакеты {i + 1}, {i + 2} были отправлены повторно -------------",
                        "blue"))
                    time.sleep(0.6)
                    queue_receiver.append(current_package_2)
                    queue_receiver.append(current_package_3)
                    print(colored(f"    Получатель: Пакеты {i + 1}, {i + 2} были приняты без ошибок", "green"))
                case 3:
                    current_package_3.remove("~")
                    print(colored(
                        f"------------- Отправитель: Пакет {i + 2} был отправлен повторно -------------",
                        "blue"))
                    time.sleep(0.6)
                    queue_receiver.append(current_package_3)
                    print(colored(f"    Получатель: Пакет {i + 2} был принят без ошибок", "green"))

        i += 3
        if i >= len(queue_sender) - 1:
            break
    stop = time.perf_counter()
    print(colored(f"Время работы: {(stop - start)*1.5}", "yellow", attrs=['underline']))





def __main__():
    question = int(input("SAW(1), SR(2), GBN(3): "))
    match question:
        case 1:
            stop_and_wait()
        case 2:
            selective_repeat()
        case 3:
            go_back_n()


if __name__ == '__main__':
    __main__()
