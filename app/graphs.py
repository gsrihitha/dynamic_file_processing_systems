import networkx as nx

def demo_workflow():
    G = nx.DiGraph()
    G.add_edge("read", "count")
    G.add_edge("count", "write")
    print("Workflow order:", list(nx.topological_sort(G)))

if __name__ == "__main__":
    demo_workflow()






