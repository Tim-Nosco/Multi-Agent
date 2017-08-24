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

def find_path(initial_edges, num_agents, agent_starts, agent_goals, s):
	n_edges = len(initial_edges)
	#vert and edge are a list of interpreted functions, it's index is the agent number
	vert = [Function("v{}".format(i),IntSort(),IntSort(), BoolSort()) for i in range(num_agents)]
	edge = [Function("e{}".format(i),IntSort(), BoolSort()) for i in range(num_agents)]

	#ensure invalid edges are not used
	for i,e in enumerate(initial_edges):
		_,_,isvalid = e
		for agent in range(num_agents):
			s.add(Implies(Not( isvalid ),
						  Not( edge[agent](i) )))
	initial_edges = [(start,end) for start,end,_ in initial_edges]

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
			elif vert_key not in agent_starts:
				#not a start state
				s.add(Not( vert[agent](*vert_key) ))

		#at least one of the start verticies must be chosen
		starts = [vert[agent](p,o) for p,o in agent_starts]
		if starts:
			s.add(Or(*starts))
		#at least one of the end verticies must be chosen
		for goal in agent_goals:
			possible = [(p,o) for p,o in connections.keys() if p in goal]
			ends = [vert[agent](p,o) for p, o in possible]
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
		#choosing a variant of a state precludes other variants
		s.add(ForAll( j,ForAll(k,ForAll(l,
						  Implies( And( vert[agent](j,k),
										l!=k),
								   Not( vert[agent](j,l) ))))))

	if str(s.check())=="unsat":
		print "unsat"
		return None

	m = s.model()

	# print "edge list", ['{}: {}'.format(i,e) for i,e in enumerate(initial_edges)]
	for agent in range(num_agents):
		print "AGENT: {}".format(agent)
		# print "edges:",["{}:{}".format(i,m.eval(edge[agent](i))) for i in range(n_edges)]
		# print "verts:",["{}:{}".format(i,m.eval(vert[agent](*i))) for i in connections]
		print "edges:",["{}=>{}".format(*initial_edges[x[0]]) for x in ((i,m.eval(edge[agent](i))) for i in range(n_edges)) if x[1]]
		print "verts:",[x[0] for x in ((i,m.eval(vert[agent](*i))) for i in connections) if x[1]]
if __name__ == "__main__":
	#graph edges:
	#e0: x0 -> x1
	#e1: x1 -> x2
	#e2: x2 -> x3
	#e3: x4 -> x5
	#e4: x5 -> x6
	#e5: x4 -> x2
	#goal: find path from x0|x4 to x3|x6
	s=Solver()
	g=[((i,0),(j,0),True) for i,j in [(0,1),(1,2),(2,3),(4,5),(5,6),(4,2)]]
	find_path(g,2,[(0,0),(4,0)],[[3,6]],s)

	s = Solver()
	g = [((0,0),(1,0),True),((1,1),(2,0),True)]
	find_path(g,1,[(0,0)],[[2]],s)