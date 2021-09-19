import  RV_graph

class RTV_graph :

    def __init__(self,rv_graph):
        self.graph = rv_graph

    def algo1(self,vehicleList):
        tao = [] # Tao is epmty list
        taoK = [] #Tao trips of size k
        for  v in vehicleList :
            taoK.clear()
            for rve in self.graph.rvEdges :
                trip =


