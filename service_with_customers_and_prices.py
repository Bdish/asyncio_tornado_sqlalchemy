from tornado.web import RequestHandler
import tornado as tornado
from config import logging
from config import config
import json


class CustomerControllers(RequestHandler):
    def get(self):
        #logging.critical("request.text: " + self.request.body.decode('utf-8'))
        try:
            self.set_status(200)
            customer = {
                'customer': 'Martin',
                'price': 100
            }
            json_body = json.dumps(customer)
            self.write(json_body)
        except Exception as e:
            logging.critical("Error on the customer server "+str(e))
            self.set_status(500)
            self.write("Error on the customer server "+str(e))


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/(favicon.ico)', tornado.web.StaticFileHandler, {"path": ""}),
            (r'/', CustomerControllers),
        ]
        settings = {
        }
        super(Application, self).__init__(handlers, **settings)


if __name__ == "__main__":
    app = Application()
    app.listen(config.get("customer_controllers", "port"), config.get("customer_controllers", "host"))
    tornado.ioloop.IOLoop.instance().start()
