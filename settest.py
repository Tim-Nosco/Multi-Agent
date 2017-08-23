from z3 import *

A = Function("A",IntSort(), BoolSort())
B = Function("B",IntSort(), BoolSort())
C = Function("C",IntSort(), BoolSort())
D = Function("D",IntSort(), BoolSort())

s = Solver()

x = Int('x')
s.add(ForAll( x, 
            Implies( Or( A(x), 
                         B(x) ),    #A union B is a subset of C
                     C(x) )))

e = Const('e', IntSort())

s.add( And( B(e),                   #An element of B is not in A
            Not( A(e) ) ) )

s.add(ForAll( x,
            Implies( D(x),          #D is a subset of C
                    C(x) )))

s.add(ForAll( x,
            Implies( Not( D(x) ),   #C is a subset of D
                    Not( C(x) ))))

s.add(B(0))
s.add(B(1))
s.add(B(2))

s.check()
m = s.model()
print "Is e an element of D?"
print m.eval(D(e))

s.add( Not( And( ForAll( x,         #A is a subset of D
                        Implies( A(x), D(x) )),
                 Exists( x,         #D contains an element not in A
                        And( D(x), Not( A(x) ) )))))
print "Now proving that A is a strict subset of D"
print s.check()