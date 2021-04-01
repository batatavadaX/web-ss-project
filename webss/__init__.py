import sys
from fastapi import FastAPI
from loguru import logger
from configparser import ConfigParser
from os import environ
from pydolphin import dolphin

logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>"
)

config = ConfigParser()
config.read('config.ini')

app = FastAPI()
dolphin.swim()
