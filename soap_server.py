from flask import Flask
from spyne import Application, rpc, ServiceBase, Integer
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from datetime import datetime

app = Flask(__name__)

class CalculatorService(ServiceBase):
    @rpc(Integer, Integer, _returns=Integer)
    def add(ctx, x, y):
        return x + y
    
    @rpc(_returns=datetime)
    def server_time(ctx):
        return datetime.now()

    @rpc(Integer, Integer, _returns=Integer)
    def multiply(ctx, x, y):
        return x * y

soap_app = Application([CalculatorService], 
                       'ejemploSOAP', 
                       in_protocol=Soap11(validator='lxml'), 
                       out_protocol=Soap11())
wsgi_app = WsgiApplication(soap_app)

@app.route("/")
def index():
    return "Servidor SOAP ejecutándose en Azure App Service"

app.wsgi_app = wsgi_app

if __name__ == '__main__':
    app.run()
