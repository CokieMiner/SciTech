import heapq

def dijkstra(grafo, inicio):

    #Inicilização:

    distancias = {vertice: float('inf') for vertice in grafo}
    distancias[inicio] = 0
    heap = [(0, inicio)]

    #Implementação do Algorítmo dijktra

    while heap:              #enquanto houver vertices por processar
        dist_atual, vertice = heapq.heappop(heap)
        if dist_atual > distancias[vertice]: 
            continue
        for vizinho, peso in grafo[vertice].items():
            nova_dist = dist_atual + peso
            if nova_dist < distancias[vizinho]:
                distancias[vizinho] = nova_dist
                heapq.heappush(heap, (nova_dist, vizinho))        #adiciona o vizinho na fila de prioridade
        return distancias