from z3 import *

#graph edges:
#e0: x0 -> x1
#e1: x1 -> x2
#e2: x2 -> x3
#e3: x1 -> x4
#e4: x1 -> x5

#goal: find path from x0 to x3

class Vert:
	def __init__(self,n):
		self.n=n
		self.start_edges=set()
		self.end_edges=[]
	def start(self,edge_num):
		self.start_edges.add(edge_num)
	def end(self,edge_num):
		self.end_edges.append(edge_num)

def find_path(initial_edges):
	n = len(initial_edges)+1

	def build_edges(initial_edges):
		nodes = [Vert(i) for i in range(len(initial_edges)+1)]
		for i,e in enumerate(initial_edges):
			start,end = e
			nodes[start].start(i)
			nodes[end].end(i)
		return nodes

	connections = build_edges(initial_edges)

	vert = [Bool("x{}".format(i)) for i in range(n)]
	# vert = Function('v',IntSort(), IntSort(), IntSort(), BoolSort())
	edge = [Bool("e{}".format(i)) for i in range(n-1)]

	s = Solver()

	for i,e in enumerate(initial_edges):
		start,end = e
		s.add( Implies( edge[i],
					  And( vert[start],
					  	   vert[end] )))
		exclusive_edges = connections[start].start_edges.difference(set([i]))
		exclusive_edges = [edge[x] for x in exclusive_edges]
		if exclusive_edges:
			s.add( Implies( edge[i],
						  Not( Or( *exclusive_edges ))))

	for node in connections:
		possible_sources = [edge[x] for x in node.end_edges]
		if len(possible_sources) == 1:
			s.add( Implies( vert[node.n],
						  possible_sources[0] ))
		elif possible_sources:
			s.add( Implies( vert[node.n],
						  Or( *possible_sources )))

	s.add(vert[0])
	s.add(vert[3])
	s.check()

	m = s.model()

	print "edges:",[m.eval(edge[i]) for i in range(n-1)]
	print "verts:",[m.eval(vert[i]) for i in range(n)]

find_path([(0,1),(1,2),(2,3),(1,4),(1,5)])
"""
python trivial_path_auto.py
edges: [True, True, True, False, False]
verts: [True, True, True, True, False, False]
"""
