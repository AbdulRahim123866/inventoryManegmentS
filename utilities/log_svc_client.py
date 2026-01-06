import json
import logging
import os
import time
from datetime import datetime

from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler, MemoryHandler


class ConfigHandler:
  def __init__(self):
    pass

  @staticmethod
  def LoadConfig(path):
    with open(path, 'r') as f:
      data = json.load(f)
    return ConfigHandler(**data)


from dataclasses import dataclass


@dataclass
class ConfigHandler:
  log_dir: str
  level: str

  @staticmethod
  def LoadConfig(path):
    with open(path, 'r') as f:
      data = json.load(f)
    return ConfigHandler(
      data.get('log_dir','logs'),
      data.get("level",'INFO'),
    )



class CustomLogger(logging.Logger):
  def __init__(self, service_name, config: ConfigHandler,):
    super().__init__(service_name)
    self.service_name = service_name
    self.config = config
    self._create_directories()
    self._attach_handlers()

  def _attach_handlers(self):
    time = f"{datetime.now():%Y%m%d-%H%M}"
    filename = f"{self.service_name}_{time}.log"
    handlers = logging.FileHandler(
      filename=os.path.join(self.config.log_dir, filename),
      encoding='utf-8'
    )

    handlers.setLevel(self.config.level)
    handlers.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    self.addHandler(handlers)

    # handlers = TimedRotatingFileHandler(filename=os.path.join(self.config.log_dir, filename), interval=1, when='s', backupCount=10)
    # handlers.setLevel(self.config.level)
    # handlers.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    # handlers.prefix = f"{self.service_name}_"
    # handlers.suffix = f"{datetime.now():%M}.log"
    # self.addHandler(handlers)

    pass

  def _create_directories(self):
    if os.path.exists(self.config.log_dir):
      return False
    try:
      os.makedirs(self.config.log_dir)
      return True
    except Exception as e:
      return False


def get_logger(service_name, path):
  config = ConfigHandler.LoadConfig(path)
  logger = CustomLogger(service_name, config)
  return logger

if __name__ == "__main__":

  logger = get_logger(service_name='EoD', path='../configs/config.json')


  while True:
    logger.info('test')
    logger.debug('test')
    logger.warning('test')
    logger.error('test')
    logger.critical('test')
    # time.sleep(1)