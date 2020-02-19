
import os
import sys

class Tank:
    def __init__(self, name, max_cap, lazy):
        self.name = name
        self.capacity = max_cap
        self.lazy = lazy
        self.beer = None
        self.interval = [ (-float("inf"), float("inf")) ]


class Query:
    def __init__(self, beer, start, end, amount):
        self.beer = beer
        self.start = start
        self.end = end
        self.amount = amount

def is_intersected(interval1, interval2):
    return False if interval2[0] > interval1[1] or interval1[0] > interval2[1] else True

def top_down(orders , tanks):
    sorted_orders = sorted(orders, key =  lambda orden : orden.start, reverse=True)
    print( [(x.cheve, x.start, x.end) for x in sorted_orders] )

    for order in orders:
        
        feasible_tanks = [tank for tank in tanks if tank.beer == order.beer and tanks.capacity != 0]
        feasible_tanks += [tank for tank in tanks if tank == None and not is_intersected( tanks.interval, [order.start, order.end] ) ]
        

    return    



if __name__ == "__main__":

    with open('query.txt', 'r', encoding="utf8") as file:
        #print(file.readlines())
        n_queries, n_tanks = map(int, file.readline().split(' '))
        queries = []
        tanks = []
        for i in range(n_queries):
            query = file.readline().split(' ')
            query = Query( query[0], int(query[1]), int(query[2]) , int(query[3]))
            queries.append(query)
            print(query.beer, query.start, query.end, query.amount)

        for i in range(n_tanks):
            name, capacity = file.readline().split(' ')
            tank = Tank(name, int(capacity), 30)
            tanks.append(tank)
            print(tank.name, tank.capacity, tank.beer, tank.interval)

    for query1 in queries:
        for query2 in queries:
            print( (query1.start, query1.end), (query2.start, query2.end))
            print(is_intersected([query1.start, query1.end], [query2.start, query2.end]) )
    #top_down(queries, tanks)