import sqlite3
import pipeline_config
import json
import logging


class WriterServiceHandler:
    insert_query = "insert into products(title, price, in_stock, url) values " \
                   "('{title}', '{price}', '{in_stock}', '{url}')"

    def __init__(self):
        self.conn = sqlite3.connect(pipeline_config.DB_LOCATION)
        self.json_file = open(pipeline_config.JSON_DUMP, 'w')

    def __del__(self):
        self.conn.close()
        self.json_file.close()

    def ping(self):
        logging.info("ping")

    def sqlite_writer(self, product):
        sql = self.insert_query.format(title=product.title, price=product.price, in_stock=product.in_stock,
                                       url=product.url)
        self.conn.execute(sql)

    def json_line_writer(self, product):
        d = {"title": product.title, "price": product.price, "in_stock": product.in_stock, "url": product.url}
        dump = json.dumps(d)
        self.json_file.write(dump)

    def write(self, product):
        self.sqlite_writer(product)
        self.json_line_writer(product)
