from model.model import Model

mymodel = Model()

mymodel.buildGraph(2014, 2016)

print(f"Nodi: {mymodel.getNumNodes()}")
print(f"Archi: {mymodel.getNumEdges()}")