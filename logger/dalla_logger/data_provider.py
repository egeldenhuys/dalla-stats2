import logging
import MySQLdb
import time
import copy
from typing import List, Dict, Tuple
from datetime import datetime

from models import DeviceRow, HistoryRow, DatabaseMap
from router_api import DeviceInfo

logger = logging.getLogger(__name__)


class DataProvider(object):

    def __init__(self, host: str, user: str, passwd: str, db: str) -> None:
        self.dbm = DatabaseMap()

        self.host = host
        self.username = user
        self.password = passwd
        self.database = db
        logger.debug('Connecting to database...')
        self.conn = None
        self.cursor = None

        try:
            self.conn = MySQLdb.connect(host=host, passwd=passwd,
                                        db=db, user=user)
            self.cursor = self.conn.cursor()
        except MySQLdb.OperationalError:
            logging.error('Cannot connect to database at %s' % host,
                          exc_info=False)

    def __del__(self):
        try:
            self.conn.close()
        except AttributeError:
            logger.warning('No database connection to close')

    def is_connected(self):

        if not self.conn or not self.cursor:
            logger.debug('self.conn or self.cursor was None')
            return False

        try:
            self.cursor.execute("SELECT VERSION()")
            results = self.cursor.fetchone()
            if results:
                return True
            else:
                return False
        except MySQLdb.Error:
            logger.debug('No connection to database')

        return False

    def flatten_device_rows_exclude(self, devices: Dict[str, DeviceRow]) -> \
            List[Tuple[str, int, int, int, int]]:
        """Returns a 2D array

            0: mac
            1: person_id
            2: total_bytes
            3: on_peak
            4: off_peak
        """

        result: List[Tuple[str, int, int, int, int]] = list()

        for mac, device in devices.items():
            if device.id == -1:
                result.append((
                    device.mac_address,
                    device.person_id,
                    device.total_bytes,
                    device.on_peak,
                    device.off_peak
                ))

        return result

    def insert_into_device_table(self, devices: Dict[str, DeviceRow]):
        """Insert the given device rows into the device table

        Only inserts if the id == -1
        """
        logger.debug('Inserting devices into database')

        if not devices:
            return None

        for mac, dev in devices.items():
            logger.debug(dev)

        flat: List[
            Tuple[str, int, int, int, int]] = self.flatten_device_rows_exclude(
                devices)

        self.cursor.executemany("""INSERT INTO {0} ({1}, {2}, {3}, {4}, {5})
                            VALUES (%s, %s, %s, %s, %s)"""
            .format(
                self.dbm.device['table_name'],
                self.dbm.device['mac_address'],
                self.dbm.device['person_id'],
                self.dbm.device['total_bytes'],
                self.dbm.device['on_peak'],
                self.dbm.device['off_peak']),
                flat)

        self.conn.commit()

    def convert_to_device_row(self, devices: Dict[str, DeviceInfo]) -> Dict[
        str, DeviceRow]:
        """Convert device info into device rows

        Ids are set to -1
        """

        device_rows: Dict[str, DeviceRow] = dict()

        for mac in devices:
            device_rows[mac] = DeviceRow(-1, devices[mac].mac_address, 1,
                                         devices[mac].total_bytes, 0, 0)

        return device_rows

    def update_device_table(self, devices: Dict[str, DeviceRow]) -> None:
        """Update or insert devices"""

        # TODO(egeldenhuys): Remove hardcode
        total_on = 0
        total_off = 0

        self.insert_into_device_table(devices)

        for mac, device in devices.items():
            total_on += device.on_peak
            total_off += device.off_peak

            if device.id != -1:
                logger.debug('Updating device {0}'.format(device))
                self.cursor.execute("""UPDATE {0}
                                    SET {1} = {2}, {3} = {4}, {5} = {6}, 
                                    {7} = {8}
                                    WHERE {9} = {10}""".format(
                        self.dbm.device['table_name'],
                        self.dbm.device['person_id'],
                        device.person_id,
                        self.dbm.device['total_bytes'],
                        device.total_bytes,
                        self.dbm.device['on_peak'],
                        device.on_peak,
                        self.dbm.device['off_peak'],
                        device.off_peak,
                        self.dbm.device['id'],
                        device.id))

        self.cursor.execute("""UPDATE person SET on_peak = %s, off_peak = %s
                              WHERE id = 1""", (total_on, total_off))

        self.conn.commit()

    def calculate_deltas(self, devices_old: Dict[str, DeviceRow],
                         devices_new: Dict[str, DeviceRow]) -> Dict[
        str, DeviceRow]:
        """Calculate the on peak and off peaks using the current time

        If new is not in old, we do not care
        New always needs to be in result
        Returns:
            Dict with the updated on and off peak with the total bytes of
            devices_new
            """
        result: Dict[str, DeviceRow] = dict()

        for mac in devices_new:
            result[mac] = copy.deepcopy(devices_new[mac])
            delta: int = result[mac].total_bytes  # default delta

            if mac in devices_old:
                result[mac] = copy.deepcopy(devices_old[mac])
                result[mac].total_bytes = devices_new[mac].total_bytes

                delta = devices_new[mac].total_bytes - devices_old[
                    mac].total_bytes

                if delta < 0:
                    logger.warning('Delta = {0} Old = {1} New = {2}'.format(delta, devices_old[mac], devices_new[mac]))
                    delta = result[mac].total_bytes
                    logger.warning('Correcting to {0}'.format(delta))

            time_utc = datetime.utcnow()
            # 22 UTC = 0h SAST
            # 4 UTC = 6h SAST
            logger.debug('Hour = {0}'.format(time_utc.hour))
            if 22 <= time_utc.hour < 4:
                result[mac].off_peak += delta
            else:
                result[mac].on_peak += delta

        return result

    def get_device_rows(self, devices: Dict[str, DeviceInfo]) -> Dict[
        str, DeviceRow]:
        """Find the given devices in the database.

        Returns:
            Found rows
        """
        logger.debug('Getting device rows from database')
        if not devices:
            logger.warning('No devices found')
            return dict()

        macs_info: List[str] = ['"{0}"'.format(mac) for mac in
                                list(devices.keys())]

        self.cursor.execute(
                """SELECT {0}, {1}, {2}, {3}, {4}, {5} FROM {6} WHERE {7} IN 
                ({8})"""
                    .format(self.dbm.device['id'],
                            self.dbm.device['mac_address'],
                            self.dbm.device['person_id'],
                            self.dbm.device['total_bytes'],
                            self.dbm.device['on_peak'],
                            self.dbm.device['off_peak'],
                            self.dbm.device['table_name'],
                            self.dbm.device['mac_address'],
                            ', '.join(macs_info)))

        results = self.cursor.fetchall()

        db_devices: Dict[str, DeviceRow] = dict()

        logger.debug('Devices found:')
        for row in results:
            db_devices[row[1]] = DeviceRow(row[0], row[1], row[2], row[3],
                                           row[4], row[5])
            logger.debug(db_devices[row[1]])

        return db_devices

    def convert_to_history_rows(self, devices: Dict[str, DeviceInfo]):
        """Convert device infos to History Rows"""

        result: Dict[str, HistoryRow] = dict()

        for mac, device in devices.items():
            result[mac] = HistoryRow(-1, -1, device.ip_address,
                                     device.record_time, device.total_bytes)
        return result

    def flatten_history_rows_exclude(self, devices: Dict[str, HistoryRow]) -> \
            List[Tuple[int, str, int, int]]:

        """Flatten for multiple inserts

        0: device_id
        1: ip_address
        2: record_time
        3: total_bytes
        """

        result: List[Tuple[int, str, int, int]] = list()

        for mac, device in devices.items():
            if device.id == -1:
                result.append((
                    device.device_id,
                    device.ip_address,
                    device.record_time,
                    device.total_bytes,
                ))

        return result

    def insert_into_history_table(self, devices: Dict[str, HistoryRow]):
        """Insert transactions with id == -1 into history table"""

        logger.debug('Inserting into history table')

        for mac, device in devices.items():
            logger.debug(device)

        if not devices:
            return None

        flat: List[
            Tuple[int, str, int, int]] = self.flatten_history_rows_exclude(
            devices)

        self.cursor.executemany("""INSERT INTO {0} ({1}, {2}, {3}, {4})
                                   VALUES (%s, %s, %s, %s)"""
            .format(
                self.dbm.history['table_name'],
                self.dbm.history['device_id'],
                self.dbm.history['ip_address'],
                self.dbm.history['record_time'],
                self.dbm.history['total_bytes']),
                flat)

        self.conn.commit()

    def update_history_table(self, devices: Dict[str, DeviceInfo]):
        """Insert into the history table"""

        devices_db: Dict[str, DeviceRow] = self.get_device_rows(devices)
        history_rows: Dict[str, HistoryRow] = self.convert_to_history_rows(
                devices)

        for mac, device in devices_db.items():
            if mac in history_rows:
                history_rows[mac].device_id = device.id

        self.insert_into_history_table(history_rows)

    def update_database(self, devices: Dict[str, DeviceInfo]):
        """Entry point for updating all tables"""

        logger.debug('Performing database update')

        for mac, device in devices.items():
            logger.debug(device)

        devices_old: Dict[str, DeviceRow] = self.get_device_rows(devices)
        devices_new: Dict[str, DeviceRow] = self.convert_to_device_row(devices)
        devices_delta = self.calculate_deltas(devices_old, devices_new)
        self.update_device_table(devices_delta)
        self.update_history_table(devices)
