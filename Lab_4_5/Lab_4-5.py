"""В каждом роутере должен быть обреззанная таблица маршрутизации(содержит только всевозможные узлы до которых есть
путь и ближайшую к ним вершину по расстоянию) или полную таблицу. !!!ИЛИ!!! Когда пакет переходит в роутер вычислять
в роутере кратчайюший путь до вершины target, которая указана в пакете, и передавать пакет в следующи маршрутизатор,
который указан в этом пути

"""
"""
Случайным образом генерируется source вершина, так как пакет содержит в себе только target, id и priority_class
С помощью потоков граф, пакет и source передаются в метод маршрутизации.
Если пути нет, то пакет потерялся. Или, если возникают какие-то проблемы с очередью, тоже пакет потерялся.
В каждом узле, в который попадает тот или иной пакет, вычиляется путь до target узла, пакет передается следующему маршрутизатору в этом пути,
и извлекается из очереди текущего роутера.
Передача пакетов и их фильтрация происходит на уровне общей очереди пакетов. То есть есть очредь всех пакетов, отсортированная по увеличению их класса проиоритетности
и в сеть в первую очредь попадают именно эти, самые приоритетные пакеты, обрабатываются они тоже в первую очередь.
Графики:
1) первым появляется график времени обработки пакетов. По оси x - id пакета, y - среднее время обработки пакета
2) график средней длинны очредей, по оси х - количество пакетов, у - средняя длина очередей в данный момент.

"""

import random
import threading
import time

import matplotlib.pyplot as plt
import networkx as nx


def generator_graph(type_topology: int, count_nodes: int, count_links: int):
    queue = []
    adjacency_list = []
    graph = nx.Graph()
    if type_topology == 1:  # ring

        for i in range(count_nodes):
            graph.add_node(i, queue=queue, adjacency_list=adjacency_list)

        for i in range(0, count_nodes, 1):
            graph.add_edge(i, i + 1, weight=random.randint(0, 9999))

        graph.add_edge(0, count_nodes, weight=random.randint(0, 9999))

    elif type_topology == 2:  # star

        for i in range(count_nodes):
            graph.add_node(i, queue=queue, adjacency_list=adjacency_list)

        random_node = random.randint(0, count_nodes)

        for i in range(count_nodes):
            if random_node == i:
                continue
            else:
                graph.add_edge(i, random_node, weight=random.randint(0, 9999))

    elif type_topology == 3:  # random

        for i in range(count_nodes):
            graph.add_node(i, queue=queue, adjacency_list=adjacency_list)

        for j in range(count_nodes):
            for i in range(count_links):
                rand = random.randint(0, count_nodes)
                if rand == j:
                    continue
                else:
                    graph.add_edge(j, rand, weight=random.randint(0, 9999))

    return graph


def generator_of_package(graph, count_nodes):
    return random.randint(0, count_nodes)


def package_treatment():
    time_sleep = random.random() * 1.5
    time.sleep(time_sleep)
    return round(time_sleep)


def create_graphics(treatment, list_of_length_queue: list):  # рисует графики
    x_treatment = []
    y_treatment = []
    for i in treatment:
        x_treatment.append(i)
        y_treatment.append(treatment[i])
    x_treatment.sort()
    gpraphik_one = plt.plot(x_treatment, y_treatment)
    plt.show()
    x_treatment.clear()
    for i in range(len(list_of_length_queue)):
        x_treatment.append(i)
    gpraphik_two = plt.plot(x_treatment, list_of_length_queue)
    plt.show()


def draw_and_save(graph, type_topology: int):
    # arrows=True - указать в сгнатуре draw(), чтобы отобразилось направление ребра
    if type_topology == 1:  # ring
        nx.draw_circular(graph, with_labels=True, node_size=230, label={'weight'}, node_color="red")
    elif type_topology == 2:  # star
        nx.draw(graph, with_labels=True, node_size=230, node_color="red")
    elif type_topology == 3:  # random
        nx.draw(graph, with_labels=True, node_size=230, node_color="red")

    plt.savefig("graph.png")
    plt.show()


delivered_package = 0
lost_package = 0

dict_of_package_treatment = {}
list_of_length_queue = []

locker = threading.Lock()


def routing_executor(graph, package: list, source_node: int):
    global dict_of_package_treatment, list_of_length_queue, lost_package, delivered_package
    # if package in graph.nodes[source_node]['queue']:
    #     print('##### This package is already in this queue. #####')
    try:
        graph.nodes[source_node]['queue'].append(package)
    except KeyError:
        lost_package += 1
    #cортировка очереди текущего узла, по возрастанию приоритетности пакета. Берется самый приоритетный, который будет первым и начинает обрабатываться.
    try:
        graph.nodes[source_node]['queue'].sort(key=lambda x: x[2])
    except KeyError:
        pass
    try:
        package = graph.nodes[source_node]['queue'].pop(0)
    except KeyError:
        pass
    print(f"{package[1]}'th package with class {package[2]} in node {source_node},{threading.currentThread().name}")
    # график по обработке будет стоиться по одной оси - id  пакета, по другой - среднее время его обработки
    dict_of_package_treatment[package[1]].append(package_treatment())
    summator = 0  # счетчик совокупной длинны очередей
    for i in range(len(graph.nodes)):
        try:
            summator += len(graph.nodes[i]['queue'])
        except KeyError:
            summator += 0
    list_of_length_queue.append(
        summator / len(graph.nodes))  # график будет строиться только по одно оси, будет график средних длинн очредей
    while True:
        try:
            path = nx.dijkstra_path(graph, source_node, package[0])  # путь от текущего узла до target
        except:
            print(
                f"########## there is no way to this node from this node, {package[1]}'th package with class {package[2]} in node {source_node} is lost,{threading.currentThread().name}! ###########")
            lost_package += 1
            break
        if package[0] == source_node:
            print(
                f"\n------------{package[1]}'th package with class {package[2]} is delivered, node {source_node},  {threading.currentThread().name}------------------------------------------\n")
            delivered_package += 1
            # try:
            #     graph.nodes[source_node]['queue'].pop(0)  # удаляем пакет из очереди
            # except KeyError:
            #     print(f"#### {package[1]}'th package is lost #####")
            #     lost_package += 1
            break
        else:
            try:
                graph.nodes[path[1]]['queue'].append(
                    package)  # добавляем пакет в очередь следующего узла в пути, если этот путь вообще есть
            except KeyError:
                print(f"#### {package[1]}'th package, class is {package[2]}, is lost #####")
                lost_package += 1
        # try:
        #     graph.nodes[source_node]['queue'].pop(0)  # удаляем пакет из очереди
        # except KeyError:
        #     pass
        source_node = path[1]  # переобпределяем переменную, присвяивая значение следующего узла в пути.

def main():
    type_topology = int(input("write type of topology 1 - ring, 2 - star, 3 - random: "))
    count_nodes = int(input("write count nodes: "))
    count_links = None

    if type_topology == 3:
        count_links = int(input("write count of links at the node: "))

    graph = generator_graph(type_topology, count_nodes, count_links)
    draw_and_save(graph, type_topology)
    count_package = int(input("write count package: "))
    list_of_threads = []
    packages_list = []
    for i in range(count_package):
        packages_list.append([generator_of_package(graph, count_nodes), i, random.randint(0, 89)])
    #packages_list.sort(key=lambda x: x[2])#Сортируем список по третьему элементу, то есть по приоритетности пакета

    for i in range(count_package):
        package = packages_list.pop(0)
        print(f"{i}'th package is {package}, class is {package[2]}")
        source_node = random.randint(0, len(graph.nodes))
        dict_of_package_treatment[package[1]] = []
        thr = threading.Thread(target=routing_executor, args=(graph, package, source_node),
                               name=f"thread-{i}")
        list_of_threads.append(thr)
        thr.start()

    for i in list_of_threads:
        i.join()

    print(list_of_length_queue)
    # for i in dict_of_package_treatment:
    #     print(f"{i} -- {dict_of_package_treatment[i]}")
    print(f"delivered packages: {delivered_package}")
    print(f"packages lost: {count_package - delivered_package}")
    print(f"length of queue. middle:{sum(list_of_length_queue)/ len(list_of_length_queue)}")
    #create_graphics(dict_of_package_treatment, list_of_length_queue)


if __name__ == "__main__":
    main()

