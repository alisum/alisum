import csv
import math
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import collections
from math import inf

# чтение списка смежности
def read_list():
	csv_path = "vk_friends_list.csv"
	results = {}
	with open(csv_path) as csvfile:
		reader = csv.reader(csvfile, delimiter=";" )
		for row in reader: 
			results[row[0]] = row[1:]
	return results

# сильные компоненты связности
def strong_comp(graph, start):

	# находим обратный граф
    def reverse(graph):
        result = {}
        for v in graph:
            result[v] = []

        for v in graph:
            for other_v in graph[v]:
                if v not in result[other_v]:
                    result[other_v].append(v)
        return result

    # дфс от вершины; в visited - все посещенные вершины, даже если были посещены из другой компоненты 
    def dfs(graph, node, visited):
        if node not in visited:
            visited.append(node)
            for n in graph[node]:
                dfs(graph,n, visited)

        return visited

    # поиск компонент сильной связности
    visited = []
    graph_r = reverse(graph)
    sorted_v = []	# массив для вершин, отсортированных по убыванию порядка выхода дфс
    res = {}		# словарь в виде 'вершина': отсортированный_выход

    while (len(sorted_v) != len (graph)):
        sorted_v = dfs(graph_r, start, visited)	# отсортировали текущую компоненту 

        # запись в словарь
        n = len(sorted_v)	
        for v in sorted_v:
            if v not in res:
                res[v] = n
                n = n - 1

        # ищем новую компоненту 
        if (len(sorted_v) != len (graph)):
            for v in graph:
                if v not in sorted_v:
                    start = v
                    break
    # сортируем полученный список вершин по убыванию выхода (данные из словаря res)
    sorted_v = sorted(res.items(), key = lambda kv:(kv[1]), reverse = True)
    # 
    res = []
    for v in sorted_v:
        res.append(v[0])

    # дфс по исходному графу
    visited, num_of_v = [], []
    num = 1
    sorted_v = []
    start = res[0]

    while (len(sorted_v) != len (graph)):
        l = len(sorted_v)	# сколько вершин пройдено
        sorted_v = dfs(graph, start, visited)
        num_of_v.append(len(sorted_v) - l)	# список количества вершин в компонентах 
        									#(из длины нового списка пройденных отнимаем то, что было до дфс)
        # проверяем, есть ли непройденные
        if (len(sorted_v) != len (graph)):
            for v in res:
                if v not in sorted_v:
                    start = v
                    break
    return len(num_of_v), num_of_v

# результат: количество слабосвзяных компонент,  массив с количеством вершин, 
# доля вершин в наибольшей компоненте, массив со списком вершин из макс компоненты 
def weak_comp(graph, start):
	stack, path, num_of_v, max_comp = [start], [], [], []
	num = 1
	while (len(path) != len(graph)):
		sub_path = []

    	#ищем компоненту слабой связности 
		while stack:
			vertex = stack.pop()
			if vertex in path:
				continue
			path.append(vertex)
			sub_path.append(vertex)
			for neighbor in graph[vertex]:
				stack.append(neighbor)

		#ищем наибольшую компоненту связности
		num_of_v.append(len(sub_path))
		if (len(sub_path) > len(max_comp)):
			max_comp = sub_path

	    #проверям, есть ли еще вершины, не принадлежащие списку пройденных (еще компоненты)
		if (len(path) != len(graph)):
			num = num + 1
			for vertex in graph:
				if vertex not in path:
					stack = [vertex]
					break
	    			    			
	return num, num_of_v, max(num_of_v)/len(graph), max_comp

# массив степеней вершин (для гистограммы, не выводится), средняя степень вершин, диаметр (+ периферийные вершины),
# радиус (+ центральные вершины), средняя длина пути между вершинами
def task_2(graph, v_list):
	deg_of_v = []
	deg_sum = 0
	cent = []
	for v in graph:
		deg_of_v.append(len(graph[v]))
		deg_sum = deg_sum + len(graph[v])

	A = to_matrix(graph)
	path_m = floyd_warshall(A)

	[d, peref_v] = diameter(path_m, v_list)
	[r, cent_v] = radius(path_m, v_list)
	return deg_of_v, deg_sum/len(graph), d, peref_v, r, cent_v, mean_path(path_m)

# задание 3, общие соседи
def common_neighbours(graph, x, y):
	n = 0
	for v_x in graph[x]:
		for v_y in graph[y]:
			if (v_x == v_y):
				n = n + 1
	return n

# задание 3, мера Жаккара
def jaccard (graph, x, y):
	v_sum = []
	for v_x in graph[x]:
		v_sum.append(v_x)
	for v_y in graph[y]:
		if v_y not in v_sum:
			v_sum.append(v_y)
	neighbor = common_neighbours (graph, x, y)
	return neighbor/len(v_sum)

# задание 3, Adamic/Adar
def adamic(graph, x, y):
	result = []
	summa = 0
	for v_x in graph[x]:
		for v_y in graph[y]:
			if (v_x == v_y):
				result.append(v_x)
	for v in result:
		if (math.log(len(graph[v])) != 0):
			summa = summa + 1/(math.log(len(graph[v])))
		else:
			summa = 0
	return summa

# задание 3, Preferential Attachment
def pref_at(graph, x, y):
	return len(graph[x]) * len(graph[y])

# список смежности в матрицу смежности
def to_matrix (graph):
	G = nx.Graph(graph)
	A = nx.to_numpy_matrix(G)
	A[A == 0] = inf
	return A

# Флойд-Уоршалл, с матрицей смежности
def floyd_warshall(graph):
    v = len(graph)
    p = np.zeros(graph.shape)
    for i in range(0,v):
        for j in range(0,v):
            p[i,j] = graph[i,j]
           
    for k in range(0,v):
        for i in range(0,v):
            for j in range(0,v):
                if p[i,j] > p[i,k] + p[k,j]:
                    p[i,j] = p[i,k] + p[k,j]
    return (p)

# Задание 2, диаметр графа (+ периферийные вершины)
def diameter(path_m, vertexes):
	result = []
	m = np.amax(path_m)
	for (idx, row) in enumerate(path_m):
		if (np.amax(row) == m):
			result.append(vertexes[idx])	# добавляем в список периферийных вершин
	return m, result

# Задание 2, радиус графа (+ центральные вершины)
def radius(path_m, vertexes):
    result = []
    mn = inf
    for (idx, row) in enumerate(path_m):
        if (np.amax(row) <= mn):
            mn = np.amax(row)

    for (idx, row) in enumerate(path_m):
        if (np.amax(row) == mn):
            result.append(vertexes[idx])	#добавляем в список центральных вершин
    return mn, result

# Задание 2, средняя длина пути
def mean_path(path_m):
	return np.mean(path_m)

# перевести ориентированный в неориентированный
def to_undirected(ver, graph):
	result = {}
	for v in ver:
		result[v] = graph[v]
		for other_v in graph:
			if v in graph[other_v] and other_v not in result[v]:
				result[v].append(other_v)

	return result

# задание 2, гистограмма степеней
def histo(degrees):
	d = {x: degrees.count(x) for x in degrees}
	plt.bar(list(d.keys()), d.values(), color='b')
	plt.show()

# центральность по степени
def degree_centr(graph):
    m = len(graph) - 1
    result = {}
    for v in graph: 
            result[v] = len(graph[v]) / m
    return result

# запись в csv файл
def to_file_csv(arr, file_name):
	with open(file_name, 'w', newline = '') as f:
	    writer = csv.writer(f, delimiter = ';')
	    for row in arr:
	       writer.writerow(row)
	f.close()

matrix = read_list()

und_matrix = to_undirected(matrix, matrix)
[strong_connected, strong_num_of_v] = strong_comp(matrix, '10015045')
[weak_connected, weak_num_of_v, max_weak, max_component] = weak_comp(und_matrix, '10015045')
graph = to_undirected(max_component,matrix)

v_list = []
for v in graph:
    v_list.append(v)

[arr_of_deg, avg_deg, g_diameter, g_peref_v, g_radius, central_v, g_mean_path] = task_2(graph, v_list)


#ВЫВОД

print ("Сильных компонент свзяности: ", strong_connected, 
    "\nКоличество вершин в сильных компонентах свзяности: ", strong_num_of_v)

print ("Слабых компонент свзяности: ", weak_connected, 
	"\nКоличество вершин в слабых компонентах свзяности: ", 
	weak_num_of_v, "\nНаибольшей компоненте принадлежит: ", max_weak)

print ("Средняя степень вершин: ", avg_deg)
print("Диаметр графа: ", g_diameter, "\nРадиус графа: ", g_radius, "\nЦентральные вершины: ", central_v, "\nПериферийные вершины: ", g_peref_v, "\nСредняя длина пути в графе: ", g_mean_path)
histo(arr_of_deg)

# ЗАДАНИЕ №3 (с записью в csv-файлы матриц получившихся результатов)

neigh, jac, ad, pref = [], [], [], []

for v in v_list:
    neigh_1, jac_1, ad_1, pref_1  = [], [], [], []
    for v_1 in v_list:
        neigh_1.append(common_neighbours(graph, v, v_1))
        jac_1.append(jaccard(graph, v, v_1))
        ad_1.append(adamic(graph, v, v_1))
        pref_1.append(pref_at(graph, v, v_1))
    neigh.append(neigh_1)
    jac.append(jac_1)
    ad.append(ad_1)
    pref.append(pref_1)

neigh = np.array(neigh)
jac = np.array(jac)
ad = np.array(ad)
pref = np.array(pref)

to_file_csv(neigh, 'common_neighbours.csv')
to_file_csv(jac, "jaccards_coeff.csv")
to_file_csv(ad, "adamic_adar.csv")
to_file_csv(pref, "pref_at.csv")

