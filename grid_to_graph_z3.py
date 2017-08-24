from z3 import *

def board_states(m,s):
	height = len(m)
	width = len(m[0])
	facings = {"up":0,"right":1,"down":2,"left":3}
	move = {'up':   lambda i,j: (i-1,j),
			'right':lambda i,j: (i,j+1),
			'down': lambda i,j: (i+1,j),
			'left': lambda i,j: (i,j-1)}
	opposite = {'up':'down',
				'down':'up',
				'left':'right',
				'right':'left'}
	def is_inbounds(i,j):
		return (i>=0) and (i<height) and (j>=0) and (j<width)
	
	edges = []
	k = 0
	for i, row in enumerate(m):
		for j, available in enumerate(row):
			pos = j+(width*i)
			for f in facings:
				start = (pos,facings[f])
				#valid directions are anywhere but where you've come from
				valid_directions = set(move.keys())
				valid_directions.discard(opposite[f])
				for v in valid_directions:
					end_i, end_j = move[v](i,j)
					if is_inbounds(end_i,end_j):
						#move one tile in any of these valid directions (if inbounds)
						end = (end_j+(width*end_i),facings[v])
						state_bool = Bool("k{}".format(k))
						s.add(Implies(Or(Not(available),
										 Not(m[end_i][end_j])),
									  Not(state_bool)))
						edges.append((start,end,state_bool))
						k+=1
						# print "{}\t B> {}".format((i,j,f),(end_i,end_j,v))

				end_i, end_j = move[f](i,j)
				for underground in range(7):
					end_i, end_j = move[f](end_i, end_j)
					if is_inbounds(end_i,end_j):
						end = (end_j+(width*end_i),facings[f]+4)
						state_bool = Bool("k{}".format(k))
						s.add(Implies(Or(Not(available),
										 Not(m[end_i][end_j])),
									  Not(state_bool)))
						edges.append((start,end,state_bool))
						k+=1
						# print "{}\t U> {}".format((i,j,f),(end_i,end_j,f))
						#Underground tunnels must end with a distinct facing
						#states with this facing can only move in the direction they face
						end_k,end_l = move[f](end_i, end_j)
						if is_inbounds(end_k,end_l):
							end2 = (end_l+(width*end_k),facings[f])
							state_bool = Bool("k{}".format(k))
							s.add(Implies(Or(Not(available),
											 Not(m[end_k][end_l])),
										  Not(state_bool)))
							edges.append((end,end2,state_bool))
							k+=1

	return edges


if __name__ == "__main__":
	a,b,c,d,e,f = Bools("a b c d e f")
	s = Solver()
	s.add(And(a,b,c,d,e))
	s.add(Not(f))

	m = [[a,b,c],
		 [d,e,f]]

	edges = board_states(m,s)

	print s.check()
	m = s.model()
	for start,end,isvalid in edges:
		print "{}\t=>{}\t{}".format(start,end,m.eval(isvalid))