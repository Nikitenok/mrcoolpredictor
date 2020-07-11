from . import model
from . import parser_data

class Predictor:

    ar = model.Arima()
    p = parser_data.Parser()
    
    def __init__(self):
        pass

    def predict(self):
        #self.p.update_data()
        self.ar.make_predictions()
    
    def get_preds(self):
        return self.ar.get_preds()




