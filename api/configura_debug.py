from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG
from logging import critical, error, warning, info, debug
from logging import basicConfig

basicConfig(
	level=INFO,
	filename='serpro.log',
	filemode='a',
    format='%(levelname)s:%(asctime)s:%(message)s'
)

