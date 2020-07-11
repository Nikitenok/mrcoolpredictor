from . import model
from . import parser_data

class Predictor:

    ar = model.Arima()
    p = parser_data.Parser()
    
    def __init__(self):
        pass

    def predict(self):
        print("0")
        self.p.update_data()
        print("1")
        self.ar.make_predictions()
    
    def get_preds(self):
        return self.ar.get_preds()




