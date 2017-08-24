from grid_to_graph_z3 import board_states
from vertex_variants import find_path
from z3 import *

# board = [[1,0,0,0],
# 		 [1,1,0,0],
# 		 [1,1,1,0],
# 		 [1,1,1,1]]
# board = [map(bool,row) for row in board]
# height = len(board)
# width = len(board[0])

# starts = [(3,0),(3,1)]
# starts = [(j+(i*width),0) for i,j in starts]
# ends = [(0,0),(3,3)]
# ends = [j+(i*width) for i,j in ends]

# print board
# print starts
# print ends

# s = Solver()
# edges = board_states(board,s)
# find_path(edges,2,starts,[ends],s)

"""
AGENT: A
edges: ['(9, 0)=>(10, 1)', '(10, 1)=>(14, 2)', '(13, 0)=>(9, 0)', '(14, 2)=>(15, 1)']
verts: [(15, 1), (9, 0), (14, 2), (13, 0), (10, 1)]
AGENT: B
edges: ['(12, 0)=>(0, 4)']
verts: [(0, 4), (12, 0)]

board = [[B,0,0,0],
		 [1,1,0,0],
		 [1,A,A,0],
		 [B,A,A,A]]
"""

# board = [[1,0,0,0,0,1],
# 		 [1,1,0,0,1,1],
# 		 [1,1,1,1,1,1],
# 		 [1,1,1,1,1,1]]
# board = [map(bool,row) for row in board]
# height = len(board)
# width = len(board[0])

# starts = [(3,0),(3,1)]
# starts = [(j+(i*width),0) for i,j in starts]
# ends = [(0,0),(0,5)]
# ends = [j+(i*width) for i,j in ends]

# print starts
# print ends

# s = Solver()
# edges = board_states(board,s)
# find_path(edges,2,starts,[ends],s)

"""
AGENT: A
edges: ['(6, 0)=>(7, 1)', '(7, 1)=>(13, 2)', '(12, 3)=>(6, 0)', '(13, 2)=>(12, 3)', '(18, 0)=>(0, 4)']
verts: [(0, 4), (6, 0), (18, 0), (7, 1), (12, 3), (13, 2)]
AGENT: B
edges: ['(17, 0)=>(5, 4)', '(19, 0)=>(20, 1)', '(20, 1)=>(21, 1)', '(21, 1)=>(22, 1)', '(22, 1)=>(23, 1)', '(23, 1)=>(17, 0)']
verts: [(5, 4), (21, 1), (20, 1), (23, 1), (17, 0), (22, 1), (19, 0)]

board = [[A,0,0,0,0,B],
		 [A,A,0,0,1,1],
		 [A,A,1,1,1,B],
		 [A,B,B,B,B,B]]
"""

board = """\
0001
0010
0100
1000
1111"""
board = [map(lambda x: bool(int(x)),row) for row in board.split()]
height = len(board)
width = len(board[0])

starts = [(4,0),(4,1),(4,2),(4,3)]
starts = [(j+(i*width),0) for i,j in starts]
end0 = [(3,0)]
end0 = [j+(i*width) for i,j in end0]
end1 = [(0,3)]
end1 = [j+(i*width) for i,j in end1]

print board
print starts
print end0,end1

s = Solver()
edges = board_states(board,s)
find_path(edges,2,starts,[end0,end1],s)