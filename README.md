## Collaborative Path Finding
![image](https://github.com/alimaharramli/multiagentdijkstra/assets/96080148/d01c0dc6-1b13-4511-9f7d-b9a11b0d8f80)

![image](https://github.com/alimaharramli/multiagentdijkstra/assets/96080148/977f8b2f-b8b2-43b8-ac7a-ba29c4cbbaff)

### A crucial aspect of the algorithm is the real-time collaboration between agents to optimize path finding. This is achieved through the following code segment:
```python
for other_agent in agents:
    if other_agent != self:
        other_path, other_distance = await other_agent.get_shortest_path(start, neighbor)
        if other_distance < new_distance:
            new_distance = other_distance
            new_path = other_path
```

- `for other_agent in agents:` iterates over all agents participating in the network.
- `if other_agent != self:` ensures that the agent does not compare paths with itself but only with other agents.
- `other_path, other_distance = await other_agent.get_shortest_path(start, neighbor)` asynchronously retrieves the shortest path and distance from the start node to the `neighbor` node, as known by the `other_agent`.
- `if other_distance < new_distance:` checks if the path known by the `other_agent` is shorter than the current best path known to the executing agent (self).
  - If true, it updates `new_distance` and `new_path` with the shorter distance and corresponding path.
