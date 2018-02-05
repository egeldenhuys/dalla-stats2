#!/bin/python

import sys
import configparser
import logging
import os
import time
from typing import Dict

from data_provider import DataProvider
import router_api
from router_api import DeviceInfo

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def print_usage():
    print('Usage:\t{0} <config_path>'.format(sys.argv[0]))
    print('\n\tconfig_path=<PATH>\tPath to config file')


def main():
    print('Starting Trigger-Update...')
    time.sleep(1) # To prevent breaking of docker-compose output

    exit_requested: bool = False

    if len(sys.argv) != 2:
        print_usage()
        return 1

    config = configparser.ConfigParser()
    config.read(sys.argv[1])

    logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s ', datefmt='%Y-%m-%d %H:%M:%S', stream=sys.stdout,
                        level=os.environ.get("LOGLEVEL", config['logging']['level']))

    data_provider: DataProvider = DataProvider(host=config['database']['host'],
                                               user=config['database']['user'],
                                               passwd=config['database']['password'],
                                               db=config['database']['database_name'])

    if not data_provider.is_connected():
        logger.error('Could not connect to database')
        logger.error('EXITING...')
        return 1

    router_session = router_api.init_session(config['router']['host'],
                                             config['router']['user'],
                                             config['router']['password'])

    while not exit_requested:
        try:
            logger.info('Fetching device info from router...')
            devices: Dict[str, DeviceInfo] = router_api.get_device_records(router_session)
            logger.info('{0} devices found'.format(len(devices)))
            logger.info('Saving to database...')
            data_provider.update_database(devices)
            logger.info('Success')

        except KeyboardInterrupt:
            logger.info('Exiting...', exc_info=False)
            return 0

        logger.info('Sleeping...')
        time.sleep(int(config['dalla_logger']['interval_minutes']) * 60)

    logger.info('Good Bye')
    return 0


if __name__ == "__main__":
    main()
