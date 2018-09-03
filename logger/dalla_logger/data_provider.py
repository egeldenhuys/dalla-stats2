import logging
import MySQLdb
import time
import copy
from typing import List, Dict, Tuple
from datetime import datetime

from models import DeviceRow, HistoryRow, DatabaseMap, PersonRow

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
        
        self.create_database_schema()

    def create_database_schema(self):
        logger.info('Creating database schema...')

        if not self.is_connected():
            logger.error('Cannot create database schema. No connection to database.')
            return

        # Copy and pasted from init-db.sql
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS person (
            id INT NOT NULL AUTO_INCREMENT,
            username VARCHAR(64) NOT NULL UNIQUE,
            password_hash VARCHAR(64),
            password_salt VARCHAR(64),
            on_peak BIGINT,
            off_peak BIGINT,
            PRIMARY KEY (id)
            )
            """
        )

        self.cursor.execute(
            """
            INSERT IGNORE INTO person (id, username, password_hash, password_salt, on_peak, off_peak)
            VALUES(1, 'Unknown', 'NO_LOGIN', 'NO_LOGIN', 0, 0)
            """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS device (
            id INT NOT NULL AUTO_INCREMENT,
            mac_address CHAR(17) NOT NULL UNIQUE ,
            person_id INT NOT NULL,
            total_bytes BIGINT,
            on_peak BIGINT,
            off_peak BIGINT,
            description VARCHAR(255),
            PRIMARY KEY (id),
            FOREIGN KEY (person_id) REFERENCES person(id)
            )
            """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS history (
            id INT NOT NULL AUTO_INCREMENT,
            device_id INT NOT NULL,
            ip_address VARCHAR(15),
            record_time INT NOT NULL,
            total_bytes BIGINT NOT NULL,
            PRIMARY KEY (id),
            FOREIGN KEY (device_id) REFERENCES device(id)
            )
            """
        )

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
            if device.device_id == -1:
                result.append((
                    device.mac_address,
                    device.person_id,
                    device.total_bytes,
                    device.on_peak,
                    device.off_peak
                ))

        return result

    def insert_into_device_table(self, devices: Dict[str, DeviceRow]):
        """Insert new devices into the device table

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

    def get_person_rows(self, devices: Dict[str, DeviceRow]) -> Dict[str, PersonRow]:
        """Get the users relating to the devices"""
        logger.debug('Getting person rows...')

        user_ids_raw: List[int] = list()

        for mac, device in devices.items():
            user_ids_raw.append(device.person_id)

        user_ids: List[str] = ['"{0}"'.format(user_id) for user_id in list(user_ids_raw)]

        self.cursor.execute(
            """SELECT {0}, {1}, {2} FROM {3} WHERE {4} IN 
            ({5})"""
                .format(self.dbm.person['id'],
                        self.dbm.person['on_peak'],
                        self.dbm.person['off_peak'],
                        self.dbm.person['table_name'],
                        self.dbm.person['id'],
                        ', '.join(user_ids)))

        results = self.cursor.fetchall()

        person_rows: Dict[int, PersonRow] = dict()

        logger.debug('Persons found')
        for row in results:
            person_rows[int(row[0])] = PersonRow(person_id=row[0], on_peak=row[1], off_peak=row[2])
            logger.debug(person_rows[int(row[0])])

        return person_rows

    def flatten_person_rows(self, person_rows: Dict[int, PersonRow]) -> \
            List[Tuple[int, int, int]]:
        """Returns a 2D array

            0: on_peak
            1: off_peak
            2: id
        """

        result: List[Tuple[int, int, int]] = list()

        for person_id, person in person_rows.items():
            result.append((
                person.on_peak,
                person.off_peak,
                person.person_id
            ))

        return result

    def update_person_table_force(self) -> None:
        """Update the user table by adding up all device values for each user"""
        logger.debug('Force updating the person table')
        devices: Dict[str, DeviceRow] = self.get_all_device_rows()
        persons: Dict[int, PersonRow] = dict()

        for mac, device in devices.items():

            if device.person_id not in persons:
                persons[device.person_id] = PersonRow(person_id=device.person_id, on_peak=0, off_peak=0)

            persons[device.person_id].on_peak += device.on_peak
            persons[device.person_id].off_peak += device.off_peak

        logger.debug('New rows:')
        for person_id, person in persons.items():
            logger.debug(person)

        flat_persons: List[Tuple[int, int, int]] = self.flatten_person_rows(persons)
        self.update_person_table_flat_rows(flat_persons)

    def update_person_table_flat_rows(self, flat_persons: List[Tuple[int, int, int]]) -> None:
        """Update the user table from flat user rows

        0: on_peak
        1: off_peak
        2: id
        """
        logger.debug('Updating person table from flat row')
        self.cursor.executemany("""UPDATE {0}
                                SET {1} = %s, {2} = %s
                                WHERE {3} = %s"""
            .format(
            self.dbm.person['table_name'],
            self.dbm.person['on_peak'],
            self.dbm.person['off_peak'],
            self.dbm.person['id']),
            flat_persons)

        self.conn.commit()

    def update_person_table(self, devices: Dict[str, DeviceRow]) -> None:
        """Update the user table using the device deltas"""
        logger.debug('Updating person table...')

        person_rows: Dict[int, PersonRow] = self.get_person_rows(devices)

        for mac, device in devices.items():
            if not device.person_id in person_rows:
                logger.error('Found a device that has no fetched user')

            time_utc = datetime.utcnow()
            if 22 <= time_utc.hour < 4:
                logger.debug(
                    'Adding {0} to off_peak for person id {1}'.format(device.delta, person_rows[device.person_id]))
                person_rows[device.person_id].off_peak += device.delta
            else:
                logger.debug(
                    'Adding {0} to on_peak for person id {1}'.format(device.delta, person_rows[device.person_id]))
                person_rows[device.person_id].on_peak += device.delta

        flat_persons: List[Tuple[int, int, int]] = self.flatten_person_rows(person_rows)

        for flattie in flat_persons:
            logger.debug('Flattie: {0}'.format(flattie))

        self.update_person_table_flat_rows(flat_persons)

    def update_device_table(self, devices: Dict[str, DeviceRow]) -> None:
        """Update or insert devices while updating the on and off peak values from the delta"""

        self.insert_into_device_table(devices)

        for mac, device in devices.items():
            if device.delta < 0:
                logger.error('Negative delta found while inserting into device table. Delta has not been calculated!')

            time_utc = datetime.utcnow()
            # Off peak hours
            # +2 (SAST)
            # 0,   1, 2, 3, 4, 5
            # (UTC)
            # 22, 23, 0, 1, 2, 3
            if 22 <= time_utc.hour or time_utc.hour <= 3:
                device.off_peak += device.delta
            else:
                device.on_peak += device.delta

            if device.device_id != -1:
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
                    device.device_id))

        self.conn.commit()

    def calculate_deltas(self, devices_old: Dict[str, DeviceRow],
                         devices_new: Dict[str, DeviceRow]) -> Dict[
        str, DeviceRow]:
        """Calculate the device deltas and set the .delta attribute"""
        result: Dict[str, DeviceRow] = dict()

        for mac in devices_new:
            result[mac] = copy.deepcopy(devices_new[mac])
            # Since we cannot assume the on or off peak, we set delta to 0
            delta: int = 0

            if mac in devices_old:
                result[mac] = copy.deepcopy(devices_old[mac])
                result[mac].total_bytes = devices_new[mac].total_bytes

                delta = devices_new[mac].total_bytes - devices_old[
                    mac].total_bytes

                if delta < 0:
                    logger.warning('Delta = {0} Old = {1} New = {2}'.format(delta, devices_old[mac], devices_new[mac]))
                    delta = result[mac].total_bytes
                    logger.warning('Correcting to {0}'.format(delta))

            result[mac].delta = delta

        return result

    def get_all_device_rows(self) -> Dict[str, DeviceRow]:
        """Fetch all device rows"""
        logger.debug('Fetching all devices...')
        # TODO(egeldenhuys): Change method if large number of devices

        self.cursor.execute(
            """SELECT {0}, {1}, {2}, {3}, {4}, {5} FROM {6}"""
                .format(self.dbm.device['id'],
                        self.dbm.device['mac_address'],
                        self.dbm.device['person_id'],
                        self.dbm.device['total_bytes'],
                        self.dbm.device['on_peak'],
                        self.dbm.device['off_peak'],
                        self.dbm.device['table_name'],
                        self.dbm.device['mac_address']))

        results = self.cursor.fetchall()

        db_devices: Dict[str, DeviceRow] = dict()

        logger.debug('Devices found:')
        for row in results:
            db_devices[row[1]] = DeviceRow(row[0], row[1], row[2], row[3],
                                           row[4], row[5])
            logger.debug(db_devices[row[1]])

        return db_devices

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
            if device.history_id == -1:
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
                history_rows[mac].device_id = device.device_id

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
        self.update_person_table_force()
        self.update_history_table(devices)
