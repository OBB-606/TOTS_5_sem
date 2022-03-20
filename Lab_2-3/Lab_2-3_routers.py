"""
Пользователь выбирает вид топологии сети, количество узлов, если топология случайна, то надо еще указать максимальное количество связей у одного узла.
Затем вводим количество пакетов, и начинается маршрутизация.
Пакет представляет собой список, где хранится путь от source до target. Путь это генерируется случайным образом в методе 'generator_of_package'
По алгоритму деукстры, причем если от 's' до 't' нет пути, то метод вызывается рекурсивно, и так до тех пор, пока
Не будет сгенерированы два узла, между которыми существует путь.
У каждого узла есть очередь из пакетов, она не ограничена. Когда пакет попадает в узел (маршрутизатор), то он должен пройти обработку.
За обработку отвечает метод treatment_package, в нем рандомится время 'обработки' пакета.
Так вот, пакет попадает в роутер и добавляется в его очередь, затем обрабатывается, затем покидает роутер, и, соответственно очередь.
Когда пакет пришел к месту назначения, то он заносится в список доставленных пакетов. Если пакет потерялся, то он заносится в список потерявшихся пакетов.
Сама маршрутизация реализована на потоках, то есть запускается поток, генерится пакет, запускается от 's' до 't',
Попутно, алгоритм маршрутизации уведосляет нас в каком узле находится сейчас пакет и какой сейчас работает поток.
Количество пакетов == количество потоков. Если пакет уже не находится в очереди конкретного маршрутизатора, то он добавляется в очеред к этому роутеру.
Проходит обработку, извлекается из очереди, переходит к следующему маршрутизатору. Если последний узел в пакете соответствует узлу,
в котором сейчас находится пакет, значит - пакет доставлен к месту назанчения.
Пока не закончится выполнение всех потоков, не появятся сообщения о статистических данных, относительно среднего времени обработки пакетов,
средней длины очереди роутеров и т.д. За это отвечает метод 'i.join'
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


def statistics(graph, count_nodes: int, list_of_time_treatment, list_of_length_queue):
    middle_degree = []
    tmp = graph.degree
    for i in range(count_nodes):
        middle_degree.append(tmp[i])
    # print("middle degree is ", sum(middle_degree) / count_nodes)
    time_middle_package = []

    for i in range(len(list_of_time_treatment)):
        for j in list_of_time_treatment[i]:
            time_middle_package.append(sum(list_of_time_treatment[i][j]) / len(list_of_time_treatment[i][j]))

    average_length_queue = list_of_length_queue
    if len(average_length_queue) != 0:
        print(
            f"max length queue - {max(average_length_queue)}, average length queue - {sum(average_length_queue) / len(average_length_queue)}")
    else:
        print("length list queue is Empty")

    # for i in range(len(time_middle_package)):
    #     print(f"time {i}'th package - {time_middle_package[i]}")
    print(f"average time a packets is on the network - {sum(time_middle_package) / len(time_middle_package)}")


def set_of_edge(graph):
    try:
        start_node = int(input("write the start node: "))
        target_node = int(input("write the target node: "))
        print("current weight this edge: ", graph.edges[start_node, target_node]['weight'])
        tmp = int(input('new weight is : '))
        graph.edges[start_node, target_node]['weight'] = tmp
        print("New weight this edge: ", graph.edges[start_node, target_node]['weight'])
        return graph.edges[start_node, target_node]['weight']
    except:
        print("such an edge does not exist")


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


def generator_of_package(graph, count_nodes):
    path = None
    source_node = random.randint(0, count_nodes)
    target_node = random.randint(0, count_nodes)
    while source_node == target_node:
        source_node = random.randint(0, count_nodes)
        target_node = random.randint(0, count_nodes)
    try:
        path = nx.dijkstra_path(graph, source=source_node, target=target_node)
    except:
        print("################# Vertices were generated to one of which there is no path! #####################")
        generator_of_package(graph, count_nodes)
    return path


def list_of_adjacency_list_this_node_creator(lst):
    list_of_nodes = []
    for i in lst:
        list_of_nodes.append(i)
    return list_of_nodes


list_of_time_treatment = []


def treatment_package():  # обработка пакета
    global list_of_time_treatment
    rand = random.random()
    # list_of_time_treatment.append({threading.currentThread().name: rand})
    time.sleep(rand)
    return round(rand, 3)


locker = threading.Lock()
list_of_length_queue = []


def routing_executor(graph, package: list, list_of_delivered_package: list):
    temp_list = []
    for i in package:
        temp_node = i
        print(f'package in node - {i}, {threading.current_thread().name}')
        try:
            if package not in graph.nodes[temp_node]['queue']:
                graph.nodes[temp_node]['queue'].append(package)
            list_of_length_queue.append(len(graph.nodes[temp_node]['queue']))
        except KeyError:
            pass
            # print(
            #     f"###################### Package in {threading.currentThread().name} is lost! #######################")

        temp_list.append(treatment_package())
        if temp_node == package[-1]:
            list_of_time_treatment.append({threading.currentThread().name: temp_list})

            print(
                f"\n------------package delivered, node {i}, {threading.currentThread().name}------------------------------------------\n")
    try:
        for i in package:
            if len(graph.nodes[i]['queue']) != 0:
                graph.nodes[i]['queue'].pop(0)
    except KeyError:
        pass
        # print(f"###################### Package in {threading.currentThread().name} is lost! #######################")
    list_of_delivered_package.append({threading.currentThread().name: package})


def reformat_adjacency_list_nodes(graph, count_nodes: int):
    for i in range(count_nodes):
        graph.nodes[i]['adjacency_list'] = list_of_adjacency_list_this_node_creator(graph.adj[i])


def executor():
    type_topology = int(input("write type of topology 1 - ring, 2 - star, 3 - random: "))
    count_nodes = int(input("write count nodes: "))
    count_links = None
    list_of_delivered_package = []

    if type_topology == 3:
        count_links = int(input("write count of links at the node: "))

    graph = generator_graph(type_topology, count_nodes, count_links)
    draw_and_save(graph, type_topology)
    reformat_adjacency_list_nodes(graph, count_nodes)
    count_package = int(input('write count package: '))
    list_of_threads = []
    for i in range(count_package):
        package = generator_of_package(graph, count_nodes)
        print(f"{i}-й пакет - {package}")
        thr = threading.Thread(target=routing_executor, args=(graph, package, list_of_delivered_package),
                               name=f"thread-{i}")
        list_of_threads.append(thr)
        thr.start()
    for i in list_of_threads:
        i.join()
    print(f'count delivered package {len(list_of_delivered_package)}')
    # print(f'list of delivered package {list_of_delivered_package}')
    print(f"count of lost package {count_package - len(list_of_delivered_package)}")
    # print(f"list of time treatment {list_of_time_treatment}")
    statistics(graph, count_nodes, list_of_time_treatment, list_of_length_queue)
    input("Press any key")


executor()
