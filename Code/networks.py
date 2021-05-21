import networkx as nx
from networkx.algorithms.centrality import group
from networkx.classes.function import degree, nodes
from pyvis.network import Network
import matplotlib.pyplot as plt
import csv
import pprint

net = Network(height = 1000, width = 1000, notebook=True)
G = nx.Graph()
pp = pprint.PrettyPrinter(indent=4)

dict_friends = {}


with open('The Friendship Paradox - A study on HU Class of 2022.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            #print(f'\tName: {row[1]}, ID: {row[2]}, Major: {row[3]}.')
            if(line_count != 0):
                dict_friends[row[1].lower()] = []
                row[4] = row[4].split(";")
                
                for i in row[4]:
                    i = i.lower()
                    dict_friends[row[1].lower()].append(i)
            line_count += 1
    print(f'Processed {line_count} lines.')


num_mapping = dict()
two_sided = dict()


for i in dict_friends.keys():
    two_sided[i] = []



edge_done = []

for i in dict_friends.keys():
    for j in dict_friends[i]:
        if j in dict_friends.keys() and i in dict_friends[j] and (i,j) not in edge_done and (j,i) not in edge_done and i != j:
            edge_done.append((i,j))
            two_sided[i].append(j)
            two_sided[j].append(i)




num = 0

num1= 0
num2= 0
num3= 0
for i in dict_friends.keys():
    num_mapping[i] = num
    if(len(two_sided[i]) >= 25):
        G.add_node(str(num), group=1)
        num1+=1
    elif(len(two_sided[i]) < 25 and len(two_sided[i]) > 15):
        G.add_node(str(num), group=1)
        num2+=1
    else:
        G.add_node(str(num), group=1)
        num3+=1 
    num+=1


edge_done = []




one_sided = 0

for i in dict_friends.keys():
    for j in dict_friends[i]:

        if j in dict_friends.keys():
            if i not in dict_friends[j]:
                one_sided += 1

        if j in dict_friends.keys() and i in dict_friends[j] and (i,j) not in edge_done and (j,i) not in edge_done and i != j:
            edge_done.append((i,j))
            G.add_edge(str(num_mapping[i]), str(num_mapping[j]))



    

degs = dict()

for i in dict_friends.keys():
    degs[i] = len(two_sided[i])


# num_friends_of_friends = 0

# for i in dict_friends.keys():
#     for j in two_sided[i]:
#         num_friends_of_friends += len(two_sided[j])

# print(num_friends_of_friends)

ind_friends = 0
deprived = 0
advantaged = 0

for i in dict_friends.keys():
    ind_friends = len(two_sided[i])
    friends_mean = 0
    for j in two_sided[i]:
        friends_mean += len(two_sided[j])

    if(ind_friends > 0):
        friends_mean = friends_mean / len(two_sided[i])

    if(ind_friends > friends_mean):
        advantaged += 1
    elif(ind_friends < friends_mean):
        deprived += 1
    

# print("The number of peopel that feel advantaged are ", advantaged)
# print("The number of peopel that feel deprived are ", deprived)


nx.write_gml(G, "graph.gml")
net.from_nx(G)
net.show_buttons(True)
net.show("graph.html")


degrees = [n for n in range(44)]
nodes_with_degree = []


deg = 0
while deg < 44:
    
    count = 0
    for i in dict_friends.keys():
        if len(two_sided[i]) == deg:
            count += 1

    nodes_with_degree.append(count)
    deg += 1 





from numpy import arange
from scipy.optimize import curve_fit
from matplotlib import pyplot

def objective(x, a, b, c):
	return a * x + b * x**2 + c

popt, _ = curve_fit(objective, degrees, nodes_with_degree)

a, b, c = popt


x_line = arange(min(degrees), max(degrees), 1)
# calculate the output for the range
y_line = objective(x_line, a, b, c)

pyplot.plot(x_line, y_line, '--', color='red')
pyplot.xlabel("Degrees")
pyplot.ylabel("Number of Nodes")
pyplot.title("Degree Distribution")
#pyplot.show()

# plt(degrees, nodes_with_degree)
# plt.show()