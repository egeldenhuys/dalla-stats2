"""Provides an API for TP-LINK AC750 Archer C20 Router"""

import base64
import time
import requests
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class DeviceInfo(object):

    def __init__(self, mac_address: str, ip_address: str, timestamp: int,
                 total_bytes: int) -> None:
        self.mac_address = mac_address
        self.ip_address = ip_address
        self.record_time = timestamp
        self.total_bytes = total_bytes


def init_session(router_ip, username, password):
    """Create a new authenticated session for admin requests"""

    logger.debug('Creating new authenticated session')
    session = requests.Session()

    raw = username + ':' + password
    encoded = base64.b64encode(raw.encode('utf-8'))

    auth = 'Basic ' + encoded.decode('utf-8')
    cookie = 'Authorization=' + auth

    session.headers = {
        'Host':
            router_ip,
        'User-Agent':
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) '
            'Gecko/20100101 Firefox/46.0',
        'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,'
            '*/*;q=0.8',
        'Accept-Language':
            'en-US,en;q=0.5',
        'Accept-Encoding':
            'gzip, deflate',
        'Content-Type':
            'text/plain',
        'Cookie':
            cookie,
        'Referer':
            'http://%s/' % router_ip,
        'Connection':
            'keep-alive'
    }

    return session


def logout(session):
    """Logout using the given session"""
    logger.debug('Sending logout request to router')

    url = 'http://{0}/cgi?8'.format(session.headers['Host'])
    session.headers.update({'Referer': 'http://{0}/MenuRpm.htm'.format(session.headers['Host'])})
    data = '[/cgi/logout#0,0,0,0,0,0#0,0,0,0,0,0]0,0\r\n'

    try:
        response = session.post(url=url, data=data)
    except KeyboardInterrupt:
        # print('[ERROR] KeyboardInterrupt during get_device_records()')
        raise

    if response.text != '[cgi]0\n[error]0':
        logger.error('Logout failed')

        if (response.text == '<html><head><title>500 Internal Server '
                             'Error</title></head><body><center><h1>500 '
                             'Internal '
                             'Server Error</h1></center></body></html>'):
            logger.error('Another admin has logged in!')
        else:
            logger.error(response.text)


def dec_str_to_ip_str(dec):
    """Convert a decimal number to an IP string"""
    bin_str = bin(int(dec))

    bin_str = bin_str[2:]
    final_str = ''

    for i in range(0, 4):
        tmp = bin_str[8 * i:8 * (i + 1)]
        tmp = int(tmp, 2)
        final_str += str(tmp) + '.'

    return final_str[:-1]


def get_devices(stats_dict_array, time_key: int) -> Dict[str, DeviceInfo]:
    """Extract valid devices from the data structure

    Args:
        stats_dict_array (?): ?
        time_key: The record_time to apply to records

    Returns:
        A list of DeviceInfo
    """

    devices: Dict[str, DeviceInfo] = dict()

    for stats_dict in stats_dict_array:
        # Only a valid device if length is 12
        if len(stats_dict) == 12:
            devices[stats_dict['macAddress']] = DeviceInfo(
                mac_address=stats_dict['macAddress'],
                ip_address=dec_str_to_ip_str(stats_dict['ipAddress']),
                timestamp=int(time_key),
                total_bytes=int(stats_dict['totalBytes']))

    return devices


def get_device_records(session) -> Dict[str, DeviceInfo]:
    """ Poll the router for the current device statistics

    These records need to be compared to a previous set to calculate the
    Delta
    """

    logger.debug('Getting device records from router')
    # Configure page specific headers
    url = 'http://%s/cgi?1&5' % session.headers['Host']
    session.headers.update(
        {'Referer': 'http://%s/mainFrame.htm' % session.headers['Host']})
    data = '[STAT_CFG#0,0,0,0,0,0#0,0,0,0,0,0]0,0\r\n[STAT_ENTRY#0,0,0,0,0,' \
           '0#0,0,0,0,0,0]1,0\r\n'

    try:
        response = session.post(url=url, data=data, timeout=1)
    except requests.ConnectionError:
        print('[ERROR] Network unreachable!')
        return {}
    except requests.ReadTimeout:
        print('[ERROR] Connection timeout!')
        return {}
    except KeyboardInterrupt:
        # print('[ERROR] KeyboardInterrupt during get_device_records()')
        raise

    raw_stats = response.text

    error = raw_stats.split('\n')

    if error[-1] != '[error]0':
        logger.error('Failed to get device records from router!')
        if (response.text == '<html><head><title>500 Internal Server '
                             'Error</title></head><body><center><h1>500 '
                             'Internal '
                             'Server Error</h1></center></body></html>'):
            logger.error('Another admin has logged in or incorrect password')
        else:
            print('  ' + response.text)

        return {}

    dict_array = []
    tmp_dict = dict()

    arr = raw_stats.split("\n")

    for i in range(0, len(arr)):

        # Loop through every line
        # If the line is a title
        #    begin split and read into dict
        # if we encounter another title
        #    insert old dict into array and start new dict and increase index

        arr[i] = arr[i].strip()

        # start of a new header
        if arr[i][0] == '[':
            dict_array.append(tmp_dict)
            tmp_dict = {}
            continue  # skip the header

        tmp = arr[i].split('=')

        # Add key=value
        if len(tmp) == 2:
            tmp_dict[tmp[0]] = tmp[1]

    # Manipulate dict array to get what we need
    init = get_devices(dict_array, int(time.time()))
    logger.debug('%i records found' % len(init))

    logout(session)

    return init
