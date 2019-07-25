"""APP runner."""
from logging.config import fileConfig
from groups_service import APP


if __name__ == '__main__':

    fileConfig('logging.config')

    APP.run(host="0.0.0.0", port=5050)
