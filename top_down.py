
import os
import sys

class Tank:
    def __init__(self, name, max_cap, lazy):
        self.name = name
        self.capacity = max_cap
        self.lazy = lazy
        self.cheve = None
        self.start = -float("inf")
        self.end = float("inf")


class Query:
    def __init__(self, cheve, start, end, amount):
        self.cheve = cheve
        self.start = start
        self.end = end
        self.amount = amount


def top_down(orders , tanks):
    sorted_orders = sorted(orders, key =  lambda orden : orden.start, reverse=True)
    print([(x.cheve, x.start, x.end) for x in sorted_orders] )
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
            print(query.cheve, query.start, query.end, query.amount)

        for i in range(n_tanks):
            name, capacity = file.readline().split(' ')
            tank = Tank(name, int(capacity), 30)
            tanks.append(tank)
            print(tank.name, tank.capacity, tank.cheve, tank.start, tank.end)

    top_down(queries, tanks)    
    