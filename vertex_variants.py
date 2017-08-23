from z3 import *

class Node:
	def __init__(self):
		self.start_edges=set()
		self.end_edges=[]
	def start(self,edge_num):
		self.start_edges.add(edge_num)
		return self
	def end(self,edge_num):
		self.end_edges.append(edge_num)
		return self

def find_path(initial_edges, num_agents, agent_starts, agent_goals):
	n_edges = len(initial_edges)
	def build_edges(initial_edges):
		nodes = dict()
		for i,e in enumerate(initial_edges):
			start,end = e
			#collect information on whether nodes are at the beginning or end of an edge
			#this allows for mutual exclusion when selecting edges that start with a node
			#it also allows the program to imply an edge must be chosen for a node to be chosen
			if start in nodes:
				nodes[start].start(i)
			else:
				nodes[start] = Node().start(i)
			if end in nodes:
				nodes[end].end(i)
			else:
				nodes[end] = Node().end(i)
		return nodes

	connections = build_edges(initial_edges)
	s = Solver()
	#vert and edge are a list of interpreted functions, it's index is the agent number
	vert = [Function("v{}".format(i),IntSort(),IntSort(), BoolSort()) for i in range(num_agents)]
	edge = [Function("e{}".format(i),IntSort(), BoolSort()) for i in range(num_agents)]

	x = Int("x")
	for agent in range(num_agents):
		for i,e in enumerate(initial_edges):
			start,end = e
			#choosing this edge means you've also chosen it's two verticies
			s.add( Implies( edge[agent](i),
						  And( vert[agent](*start),
							   vert[agent](*end) )))
			#if the start vertex of this edge is the start vertex in other edges,
			#only one of the mentioned edges can be chosen
			exclusive_edges = connections[start].start_edges.difference(set([i]))
			exclusive_edges = [edge[agent](e) for e in exclusive_edges]
			if exclusive_edges:
				s.add( Implies( edge[agent](i),
							  Not( Or( *exclusive_edges ))))
		#to choose a vertex, you must also choose an edge that points to that vertex
		#only required if such an edge exists. (consider no edge points to the start state)
		for vert_key in connections:
			node = connections[vert_key]
			possible_sources = [edge[agent](e) for e in node.end_edges]
			if possible_sources:
				s.add( Implies( vert[agent](*vert_key),
							  Or( *possible_sources )))

		#at least one of the start verticies must be chosen
		starts = [vert[agent](i,j) for i in agent_starts for j in range(4)]
		if starts:
			s.add(Or(*starts))
		#at least one of the end verticies must be chosen
		for goal in agent_goals:
			ends = [vert[agent](i,j) for i in goal for j in range(4)]
			if ends:
				s.add(Or(*ends))
	j,k,l=Ints("j k l")
	#each agent's chosen verticies must be disjoint
	for agent in range(num_agents):
		other_agents = list(range(num_agents))
		other_agents = other_agents[:agent]+other_agents[agent+1:]
		other_agents = [vert[a](j,l) for a in other_agents]
		if other_agents:
			s.add(ForAll( j,ForAll(k,ForAll(l,
						  Implies( vert[agent](j,k), 
								   Not( Or( *other_agents )))))))

	if str(s.check())=="unsat":
		print "unsat"
		return None

	m = s.model()

	print "edge list", ['{}: {}'.format(i,e) for i,e in enumerate(initial_edges)]
	for agent in range(num_agents):
		print "AGENT: {}".format(agent)
		print "edges:",["{}:{}".format(i,m.eval(edge[agent](i))) for i in range(n_edges)]
		print "verts:",["{}:{}".format(i,m.eval(vert[agent](*i))) for i in connections]

#graph edges:
#e0: x0 -> x1
#e1: x1 -> x12
#e2: x12 -> x3
#e3: x1 -> x4
#e4: x1 -> x5
#goal: find path from x0 to x3
# find_path([(0,1),(1,12),(12,3),(1,4),(1,5)],1,[0],[[3]])

#graph edges:
#e0: x0 -> x1
#e1: x1 -> x2
#e2: x2 -> x3
#e3: x4 -> x5
#e4: x5 -> x6
#e5: x4 -> x2

#goal: find path from x0|x4 to x3|x6
g=[((i,0),(j,0)) for i,j in [(0,1),(1,2),(2,3),(4,5),(5,6),(4,2)]]
find_path(g,2,[0,4],[[3,6]])
