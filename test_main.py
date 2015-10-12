
from DataBase import *
from navigator import *
import matplotlib.pyplot as plt

f = open("DataBase.txt", "r+")
        
DB = TDataBase(f)
DB.pull()

CG = CoursesGraph(DB)

print CG.get_optimal_path([1], [3,4])

#pos=nx.circular_layout(CG.Graph) # positions for all nodes
#
## nodes
#nx.draw_networkx_nodes(CG.Graph,pos,node_size=700)
#
## edges
#nx.draw_networkx_edges(CG.Graph,pos,
#                            width=6,alpha=0.5,edge_color='b',style='dashed')
#
## labels
#nx.draw_networkx_labels(CG.Graph,pos,font_size=20,font_family='sans-serif')
#
#plt.axis('off')
#plt.show()
