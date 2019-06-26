'''

This code assumes input G, is a directed graph with all it's edges
(It can have cycles, but no multiedges)

It will output, all the cross_edges

'''
cross_edges = []
adj_list = []; start_times = []; end_times = []; visited = []
time_count = 0

# def is_cross_edge(u, v):
#   s_u, e_u = start_times[u], end_times[u]
#   s_v, e_v = start_times[v], end_times[v]

#   if(s_u > e_v )

def DFS_time(node):
  global time_count
  global cross_edges

  if(visited[node]):
    return 

  visited[node] = True
  start_times[node] = time_count
  time_count += 1

  for neighbour in adj_list[node]:
    # if cross edge
    s_u, e_u = start_times[node], end_times[node]
    s_v, e_v = start_times[neighbour], end_times[neighbour]
    if(e_v != -1 and s_u > s_v):
      cross_edges.append((node, neighbour))
    if(not visited[neighbour]):
      print(node, neighbour)
      DFS_time(neighbour)

  end_times[node] = time_count
  time_count += 1
  return

def all_cross_edges(G_edges):
  global visited
  global start_times
  global end_times
  global adj_list

  G_nodes = set()
  for edge in G_edges:
    G_nodes.add(edge[0])
    G_nodes.add(edge[1])

  length = 1 + max(G_nodes)
  visited = [False] * length
  start_times = [-1] * length
  end_times = [-1] * length
  
  for i in range(length):
    adj_list.append(set())

  for edge in G_edges:
    adj_list[edge[0]].add(edge[1])

  for node in G_nodes:
    if(visited[node] == False):
      DFS_time(node)

  # for edge in G_edges:
  #   if(is_cross_edge(edge)):
  #     cross_edges.append(edge[0], edge[1])

  return cross_edges

def main():
  G_edges = [(0,1),(0,2),(0,5),(1,3),(1,4),(2,5),(3,0),(4,2),(4,6),(5,7)]
  root = 0
  weights = [1,1,11,1,1,1,12,13,1,14,1]
  print(all_cross_edges(G_edges))
  print(list(zip(start_times, end_times)))

if __name__ == '__main__':
  main()