from z3 import *

#graph edges:
#e0: x0 -> x1
#e1: x1 -> x2
#e2: x2 -> x3
#e3: x1 -> x4
#e4: x1 -> x5

#goal: find path from x0 to x3

vert = [Bool("x{}".format(i)) for i in range(6)]
edge = [Bool("e{}".format(i)) for i in range(5)]

s = Solver()

#e0: x0 -> x1
s.add( Implies( edge[0],
                And( vert[0],
                     vert[1] )))
s.add( Implies( vert[1],
                edge[0] ))

#e1: x1 -> x2
s.add( Implies( edge[1],
                And( vert[1],
                     vert[2] )))
s.add( Implies( edge[1],
                Not( Or( edge[3],
                         edge[4] ))))
s.add( Implies( vert[2],
                edge[1] ))

#e2: x2 -> x3
s.add( Implies( edge[2],
                And( vert[2],
                     vert[3] )))
s.add( Implies( vert[3],
                edge[2] ))

#e3: x1 -> x4
s.add( Implies( edge[3],
                And( vert[1],
                     vert[4] )))
s.add( Implies( edge[3],
                Not( Or( edge[1],
                         edge[4] ))))
s.add( Implies( vert[4],
                edge[3] ))

#e4: x1 -> x5
s.add( Implies( edge[4],
                And( vert[1],
                     vert[5] )))
s.add( Implies( edge[4],
                Not( Or( edge[1],
                         edge[3] ))))
s.add( Implies( vert[5],
                edge[4] ))

s.add(vert[0])
s.add(vert[3])
s.check()

m = s.model()

print [m.eval(edge[i]) for i in range(5)]
print [m.eval(vert[i]) for i in range(6)]