import sys
sys.path.append("..")

from structs.core import read_edgelist
from structs.multiplex import Multiplex

obj = Multiplex(read_edgelist("data/raw/multiplex.edgelist", network_type="MULTIPLEX"))

print(obj)
print(obj.multiplex)
print(obj.get_supraadjacency())
print(obj._Multiplex__number_of_nodes_mapping)

obj.save_edgelist("data/derived/test_save.edgelist")
obj.save_pickle("data/derived/test_save.pkl")

obj2 = Multiplex(read_edgelist("data/derived/test_save.edgelist", network_type="MULTIPLEX"))
print("{} == {}? {}".format(obj.multiplex_filepath, obj2.multiplex_filepath, obj == obj2))