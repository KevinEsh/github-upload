
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
    def __init__(self, name, beer, start, end, amount):
        self.name   = name
        self.beer   = beer
        self.start  = start
        self.split  = start
        self.end    = end
        self.amount = amount

def is_intersected(a_start, a_end, b_start, b_end):
    return not (b_start > a_end or a_start > b_end)

def any_is_intersected(intervals, start, end, lazy):
    for inter in intervals:
        if is_intersected(inter[0] - lazy, inter[1], start - lazy, end):
            return True
    return False

def top_down(orders , tanks):
    #sorted_orders = sorted(orders, key = lambda order : (order.beer, order.start, order.end), reverse=True)
    n_tanks = set()
    file = open("gov.csv", 'w')

    for order in orders:
        
        while order.amount > 0:

            try:
                feasible_tanks = [tank for tank in tanks if tank.beer == order.beer and tank.capacity > 0 \
                            and not any_is_intersected(tank.intervals, order.split, order.end, lazy=0) ]
                best = tanks.index( min( feasible_tanks, key = lambda tank : tank.capacity ) )
                
            except ValueError:
                
                try:
                    feasible_tanks = [tank for tank in tanks if tank.beer == None \
                            and not any_is_intersected(tank.intervals, order.split, tank.capacity*(order.end - order.split)//order.amount + order.split, tank.lazy) ]
                    best = tanks.index( 
                            min(
                                feasible_tanks, 
                                key = lambda tank : 
                                min(
                                    abs( (tank.capacity*(order.end - order.split)//order.amount) + order.split - tank.start),
                                    abs( order.split - tank.end)
                                    )   
                                )
                    )
                except ValueError:
                    raise Exception("There is no solution to the problem")
            
            # Beer assigned to best tank
            tanks[best].beer = order.beer
            n_tanks.add(tanks[best])

            # Calculating the max amount of beer to be assigned to the best tank. Also the split point (assuming constant flown)
            surplus_beer = min(tanks[best].capacity, order.amount)
            split = surplus_beer * (order.end - order.split) // order.amount + order.split

            tanks[best].capacity -= surplus_beer
            order.amount -= surplus_beer

            file.write(str(order.beer)+","+str(tanks[best].name)+","+str(order.split)+","+str(split)+","+str(order.name)+"\n" )

            # Updating the schedule of tank and order
            tanks[best].end = split
            tanks[best].start = order.split
            tanks[best].update_intervals()
            order.split = split

            #print(order.start, order.split, order.end)
            print(tanks[best].name, str(surplus_beer)+"/"+str(order.amount+surplus_beer), order.beer, str(tanks[best].start - tanks[best].lazy)+"~["+ str(tanks[best].start)+","+str(tanks[best].end)+"]")
            
            # Re-inicializing parameters in case this tank is full
            if tanks[best].capacity == 0:
                tanks[best].capacity = tanks[best].max_capacity
                tanks[best].beer = None   

    print("\nnumero de tanques usados", len(n_tanks), "de", len(tanks) )
    #print("Estado inicial de los tanques:")
    #for tank in tanks:
    #    print(tank.name, ":", tank.capacity, "de", tank.beer)
    return    

if __name__ == "__main__":

    with open(sys.argv[1], 'r', encoding="utf8") as file:

        n_queries, n_tanks = map(int, file.readline().split(' '))
        queries = []
        tanks = []

        # Read orders
        for i in range(n_queries):
            query = file.readline().split(' ')
            query = (query[0], int(query[1]), int(query[2]) , int(query[3]))
            queries.append(query)

        # Divide-and-Conquer 
        queries.sort( key = lambda query: (query[1], query[2]), reverse=True )
        beers = []
        orders = []
        mini = float("inf")
        for query in queries:
            mini = min(mini, query[1])
            if query[0] not in beers:
                beers.append(query[0])
        i = 0
        for beer in beers:
            for query in queries:
                if query[0] == beer:
                    orders.append( Query(i, query[0], query[1] -mini , query[2] -mini, query[3]) )
                    i += 1
        
        # Read tanks
        for i in range(n_tanks):
            name, capacity = file.readline().split(' ')
            tank = Tank(name, int(capacity), 30)
            tanks.append(tank)

    top_down(orders, tanks)