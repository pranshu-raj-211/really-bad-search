import logging

logger = logging.Logger(name=__name__, level=logging.INFO)

stream_handler = logging.StreamHandler()
file_handler=logging.FileHandler(filename='logs/app.log')

# TODO: custom log formatter
formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s')

stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)