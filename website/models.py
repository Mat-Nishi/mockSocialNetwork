from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150))
    phone = db.Column(db.String(150))
    city = db.Column(db.String(150))
    company = db.Column(db.Boolean)
   

    # notes = db.relationship('Note')

# class User:
#     def __init__(self, id, name, email, password):
#         self.id = id
#         self.name = name
#         self.email = email
#         self.password = password
    
        
# class Graph:

#     def __init__(self, size):
#         self._size = size
#         self._body = [[] for _ in range(size)]

#     def __str__(self):
#         return "Graph()"

#     def addEdge(self, u,v):
#         self._body[u].append(v)

#     def addNode(self):
#         self._body.append([])
#         self._size += 1

    
#     def bfs(self, root):
#         visited = [False for _ in range(self._size)]
#         queue = [root]
#         visited[root] = True
#         while(queue):
#             cur = queue.pop(0)
#             for node in self._body[cur]:
#                 if not visited[node]:
#                     queue.append(node)
#                     visited[node] = True