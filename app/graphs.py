import networkx as nx  # type: ignore


G = nx.DiGraph() # Creating a directed graph

G.add_node("read")
G.add_node("count")
G.add_node("write")

G.add_edge("read", "count")
G.add_edge("count", "write")

order = list(nx.topological_sort(G))
print("Workflow order:", order)
