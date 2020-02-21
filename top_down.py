
import os
import sys

class Tank:
    def __init__(self, name, max_cap, lazy):
        self.name = name
        self.capacity     = max_cap
        self.max_capacity = max_cap
        self.lazy  =  lazy
        self.beer  =  None
        self.start = -float("inf")
        self.end   = -float("inf")
        self.intervals = [(self.start, self.end)]

    def update_intervals(self):
        self.intervals.append( (self.start, self.end) )

class Query:
    def __init__(self, beer, start, end, amount):
        self.beer   = beer
        self.start  = start
        self.split  = start
        self.end    = end
        self.amount = amount

def is_intersected(a_start, a_end, b_start, b_end):
    return not (b_start > a_end or a_start > b_end)

def any_is_intersected():
    pass

def top_down(orders , tanks):
    sorted_orders = sorted(orders, key =  lambda order : (order.start, order.end), reverse=True)
    n_tanks = set()

    file = open("me.csv", 'w')

    for order in sorted_orders:
        
        while order.amount > 0:

            try:
                feasible_tanks = [tank for tank in tanks if tank.beer == order.beer and tank.capacity > 0 \
                            and not is_intersected(tank.start+tank.lazy, tank.end, order.split, order.end)]
                best = tanks.index( min( feasible_tanks, key = lambda tank : tank.capacity ) )
                #print([f.name for f in feasible_tanks] )
            except ValueError:
                #print("no feasible")
                try:
                    feasible_tanks = [tank for tank in tanks if tank.beer == None \
                            and not is_intersected(tank.start, tank.end, order.split, tank.capacity*(order.end - order.split)//order.amount + order.split) ]
                    best = tanks.index( min( feasible_tanks, key = lambda tank : abs(tank.start - tank.capacity*(order.end - order.split)//order.amount - order.split) ) )
                except ValueError:
                    raise Exception("There is no solution to the problem")
            
            n_tanks.add(tanks[best])
            # Beer assigned to best tank
            tanks[best].beer = order.beer

            # Calculating the max amount of beer to be assigned to the best tank. Also the split point (assuming constant flown)
            surplus_beer = min(tanks[best].capacity, order.amount)
            split = surplus_beer * (order.end - order.split) // order.amount + order.split

            tanks[best].capacity -= surplus_beer
            order.amount -= surplus_beer

            if split != order.split:
                file.write(str(order.beer)+","+str(tanks[best].name)+","+str(order.split)+","+str(split)+"\n" )
            else:
                file.write(str(order.beer)+","+str(tanks[best].name)+","+str(order.split)+","+str(split)+"\n" )

            # Updating the schedule of tank and order
            tanks[best].end = max(split, tanks[best].end)
            tanks[best].start = order.split - tanks[best].lazy
            order.split = max(split, order.start)

            #print(order.start, order.split, order.end)
            print(tanks[best].name, str(surplus_beer)+"/"+str(order.amount+surplus_beer), order.beer, str(tanks[best].start)+"~["+ str(tanks[best].start+tanks[best].lazy)+","+str(tanks[best].end)+"] order:(", order.start, order.split, order.end, ")")
            
            # Re-inicializing parameters in case this tank is full
            if tanks[best].capacity == 0:
                tanks[best].capacity = tanks[best].max_capacity
                tanks[best].beer = None   

    print("numero de tanques usados", len(n_tanks), "de", len(tanks) )
    print("Estado inicial de los tanques:")
    for tank in tanks:
        print(tank.name, ":", tank.capacity, "de", tank.beer)
    return    

if __name__ == "__main__":

    with open(sys.argv[1], 'r', encoding="utf8") as file:

        n_queries, n_tanks = map(int, file.readline().split(' '))
        queries = []
        tanks = []
        for i in range(n_queries):
            query = file.readline().split(' ')
            query = Query( query[0], int(query[1]), int(query[2]) , int(query[3]))
            queries.append(query)

        mini = min(queries, key = lambda query: query.start).start
        print(mini)
        queries = map(lambda query: Query(query.beer, query.start -mini , query.end -mini, query.amount), queries)
        

        for i in range(n_tanks):
            name, capacity = file.readline().split(' ')
            tank = Tank(name, int(capacity), 60)
            tanks.append(tank)

    top_down(queries, tanks)