import asyncio
import heapq
import networkx as nx
import threading

def create_graph():
    G = nx.DiGraph()
    edges = [
        ('A', 'B', 3), ('A', 'C', 5),
        ('B', 'C', 2), ('B', 'D', 6),
        ('C', 'D', 4), ('C', 'E', 6),
        ('D', 'E', 1), ('D', 'F', 5),
        ('E', 'F', 2)
    ]
    G.add_weighted_edges_from(edges)
    return G

class Agent:
    def __init__(self, name, assigned_routers, graph, lock):
        self.name = name
        self.assigned_routers = assigned_routers
        self.graph = graph
        self.lock = lock
        self.shortest_paths = {}

    async def update_shortest_path(self, source, target, path, distance):
        async with self.lock:
            if source not in self.shortest_paths:
                self.shortest_paths[source] = {}
            self.shortest_paths[source][target] = (path, distance)

    async def get_shortest_path(self, source, target):
        async with self.lock:
            return self.shortest_paths.get(source, {}).get(target, (None, float('inf')))

    async def dijkstra(self, start):
        pq = []
        heapq.heappush(pq, (0, start, [start]))

        while pq:
            distance, current_node, path = heapq.heappop(pq)

            for _, neighbor, data in self.graph.edges(current_node, data=True):
                new_distance = distance + data['weight']
                new_path = path + [neighbor]

                for other_agent in agents:
                    if other_agent != self:
                        other_path, other_distance = await other_agent.get_shortest_path(start, neighbor)
                        if other_distance < new_distance:
                            new_distance = other_distance
                            new_path = other_path

                await self.update_shortest_path(start, neighbor, new_path, new_distance)
                heapq.heappush(pq, (new_distance, neighbor, new_path))

async def multi_agent_dijkstra(agents):
    tasks = []
    for agent in agents:
        for router in agent.assigned_routers:
            task = asyncio.create_task(agent.dijkstra(router))
            tasks.append(task)
    await asyncio.gather(*tasks)

graph = create_graph()
lock = asyncio.Lock()

agent1 = Agent("Agent1", ["A", "B", "C"], graph, lock)
agent2 = Agent("Agent2", ["D", "E", "F"], graph, lock)
agents = [agent1, agent2]

async def main():
    await multi_agent_dijkstra(agents)
    path, distance = await agent1.get_shortest_path("A", "F")
    print("Shortest path from A to E:", path, "with distance:", distance)

asyncio.run(main())
