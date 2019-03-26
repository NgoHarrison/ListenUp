from logging.handlers import RotatingFileHandler
import logging
from ListenUp import app


if __name__ == "__main__":
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True, host="127.0.0.1")