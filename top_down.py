
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


class Query:
    def __init__(self, beer, start, end, amount):
        self.beer   = beer
        self.start  = start
        self.end    = end
        self.amount = amount

def is_intersected(a_start, a_end, b_start, b_end):
    return not (b_start > a_end or a_start > b_end)

def top_down(orders , tanks):
    sorted_orders = sorted(orders, key =  lambda order : order.start, reverse=True)

    for order in sorted_orders:
        
        while order.amount != 0:

            try:
                feasible_tanks = [tank for tank in tanks if tank.beer == order.beer and tank.capacity > 0 and not is_intersected(tank.start, tank.end, order.start, order.end)]
                best = tanks.index( min( feasible_tanks, key = lambda tank : tank.capacity ) )
                #print([f.name for f in feasible_tanks] )
            except ValueError:
                pass

            try:
                feasible_tanks = [tank for tank in tanks if tank.beer == None and not is_intersected(tank.start, tank.end, order.start, order.end) ]
                best = tanks.index( min( feasible_tanks, key = lambda tank : abs(tank.start - order.start) ) )
            except ValueError:
                raise Exception("There is no solution to the problem")
            
            tanks[best].beer = order.beer
            tanks[best].end = order.end
            tanks[best].start = order.start - tanks[best].lazy
            
            surplus_beer = min(tanks[best].capacity, order.amount)
            tanks[best].capacity = tanks[best].capacity - surplus_beer
            order.amount = order.amount - surplus_beer

            print(tanks[best].name, "with", str(surplus_beer)+"/"+str(order.amount+surplus_beer), "of beer", order.beer, "occupied from", tanks[best].start, "to", tanks[best].end)
            
            # Re-inicializing parameters in case this tank is full
            if tanks[best].capacity == 0:
                tanks[best].capacity = tanks[best].max_capacity
                tanks[best].beer = None   
    return    

if __name__ == "__main__":

    with open('query.txt', 'r', encoding="utf8") as file:

        n_queries, n_tanks = map(int, file.readline().split(' '))
        queries = []
        tanks = []
        for i in range(n_queries):
            query = file.readline().split(' ')
            query = Query( query[0], int(query[1]), int(query[2]) , int(query[3]))
            queries.append(query)

        for i in range(n_tanks):
            name, capacity = file.readline().split(' ')
            tank = Tank(name, int(capacity), 30)
            tanks.append(tank)

    top_down(queries, tanks)