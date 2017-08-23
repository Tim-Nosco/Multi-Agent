def board_states(m):
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
    for i, row in enumerate(m):
        for j, available in enumerate(row):
            if available:
                pos = j+(width*i)
                for f in facings:
                    start = (pos,facings[f])
                    
                    valid_directions = set(move.keys())
                    valid_directions.discard(opposite[f])
                    for v in valid_directions:
                        end_i, end_j = move[v](i,j)
                        if is_inbounds(end_i,end_j) and m[end_i][end_j]:
                            end = (end_j+(width*end_i),facings[v])
                            edges.append((start,end))
                            print "{}\t B> {}".format((i,j,f),(end_i,end_j,v))
                    end_i, end_j = move[f](i,j)
                    for underground in range(7):
                        end_i, end_j = move[f](end_i, end_j)
                        if is_inbounds(end_i,end_j) and m[end_i][end_j]:
                            end = (end_j+(width*end_i),facings[f])
                            edges.append((start,end))
                            print "{}\t U> {}".format((i,j,f),(end_i,end_j,f))


m = [[True , True , False],
     [True , True , True ]]

board_states(m)