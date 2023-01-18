from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from json import loads, load, dumps, dump
import networkx as nx
import matplotlib.pyplot as plt

# Graph Class
class Graph:
    # initializes incidence list
    def __init__(self):
        self._body = [] 
          
    # add edge (from node u to v) to incidence list
    def addEdge(self, u, v):
        self._body.append([u,v])

    # plots incidence list      
    def plot(self):
        # graph structure from networkx
        graph = nx.Graph() 
        graph.add_edges_from(self._body)
        fig = nx.draw_networkx(graph)
        # saves plot into static folder
        plt.savefig('website/static/graph_plot.jpg', bbox_inches='tight')


views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        searchTerm = request.form.get("searchTerm")
        searchType = request.form.get("searchType")
        
        if len(searchTerm)<1:
            flash("Please enter a search term", category='error')
        elif searchType=="none":
            flash("Please select a valid search type", category='error')
        else:
            return redirect(url_for('views.search_result'), code=307)

    return render_template("search.html", user=current_user)

@views.route('/search_result', methods=['GET', 'POST'])
@login_required
def search_result():
    searchTerm = request.form.get("searchTerm")
    searchType = request.form.get("searchType")

    with open("website/graph.json", 'r') as file:
        graph = load(file)
    
    with open("website/users.json", 'r') as file:
        users = load(file)
    
    visited = [False for _ in range(len(graph))]
    root = int(current_user.id)-1
    queue = [root]
    visited[root] = True
    results = []

    #bfs from user first, then bfs through disconnected nodes 
    while(len(queue)):
        cur = queue.pop(0)
        if cur != root:
            if users[str(cur)][searchType] == searchTerm:
                if int(cur) not in graph[root]:
                    aux = True
                else:
                    aux = False
                results.append((cur, users[str(cur)]['firstName'], aux))
        for node in graph[cur]:
            if not visited[node]:
                queue.append(node)
                visited[node] = True
        for i in range(len(visited)):
            if not visited[i]:
                queue.append(i)
                visited[i] = True
                break

    print(results)

    return render_template("search_result.html", user=current_user, ids=results)

@views.route('/myprofile')
@login_required
def myprofile():
    return render_template("myprofile.html", user=current_user)

@views.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    return render_template("edit.html", user=current_user)

@views.route('/forgot')
def forgot():
    return render_template("forgot.html")

@views.route('/follow-user', methods=['POST'])
@login_required
def follow_user():

    id_follow = loads(request.data)['id']
    id = current_user.id - 1

    # adds relation to graph
    with open('website/graph.json', 'r') as file:
        graph = load(file)
    graph[id].append(int(id_follow))
    with open('website/graph.json', 'w') as file:
        dump(graph, file)

    return render_template("edit.html", user=current_user)

@views.route('/relations')
@login_required
def relations():
    id = current_user.id-1
    # edits plot of relations
    with open('website/graph.json', 'r') as file:
        adj_list = load(file)
    with open('website/users.json', 'r') as file:
        users = load(file)

    graph = Graph()
    cur_name = str(id)+': '+users[str(id)]['firstName']
    for i in adj_list[id]:
        v = str(i)+': '+users[str(i)]['firstName']
        graph.addEdge(cur_name,v)

        for j in range(len(adj_list[int(i)])):
            u = str(i)+': '+users[str(i)]['firstName']
            v = str(j)+': '+users[str(j)]['firstName']
            if u != v:
                graph.addEdge(u,v)
    graph.plot()

    return render_template("relations.html", user=current_user)