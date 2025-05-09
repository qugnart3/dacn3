from SetModel import Model
from Tokenize import Tokenize

name_model = "SetModel/NotProcess/Model"
data_return = Tokenize("DataSet/all/sentsPro.txt","DataSet/test/sentiments.txt")
M = Model(name_model)
M.Eval(data_return)
