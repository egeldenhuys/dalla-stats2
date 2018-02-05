from typing import Dict, List, Tuple


class DeviceRow(object):
    """A model representing a device in the database"""

    def __init__(self, id: int, mac_address: str, person_id: int,
                 total_bytes: int, on_peak: int, off_peak: int) -> None:
        self.id = id
        self.mac_address = mac_address
        self.person_id = person_id
        self.total_bytes: int = total_bytes
        self.on_peak = on_peak
        self.off_peak = off_peak

    def __str__(self):
        return 'DeviceRow: <[id={0}, mac_address={1}, person_id={2}, ' \
               'total_bytes={3}, ' \
               'on_peak={4}, off_peak={5}]>'.format(
                self.id, self.mac_address, self.person_id, self.total_bytes,
                self.on_peak,
                self.off_peak)


class PersonRow(object):
    """A model representing a person in the database"""

    def __init__(self, id: int, username: str, on_peak: int,
                 off_peak: int) -> None:
        self.id = id
        self.username = username
        self.on_peak = on_peak
        self.off_peak = off_peak


class HistoryRow(object):
    """A row in the history table"""

    def __init__(self, id: int, device_id: int, ip_address: str,
                 record_time: int,
                 total_bytes: int) -> None:
        self.id = id
        self.device_id = device_id
        self.ip_address = ip_address
        self.record_time = record_time
        self.total_bytes = total_bytes

    def __str__(self):
        return 'HistoryRow: <[id={0}, device_id={1}, ip_address={2}, ' \
               'total_bytes={3}]>'.format(
                self.id, self.device_id, self.ip_address, self.total_bytes)


class DatabaseMap(object):
    """Collection of mappings between the data_provider and the database

    Map format:
        'static_name': ('name_in_database', <index_in_database>)

    Example:

        m = DatabaseMap()
        conn.cursor.execute('SELECT %s, %s FROM %s WHERE %s = %s'
                            .format(m.device['id'],
                                    m.device['on_peak'],
                                    m.device['table_name'],
                                    m.device['on_peak],
                                    6567567)
        r = conn.cursor.fetchone()

        result = {'id': r[0],
                 'on_peak': r[1]}
        ------
        m = DatabaseMap()
    """

    def __init__(self) -> None:
        self.database_name = 'dalla_stats'
        self.device: Dict[str, str] = {'table_name': 'device',
                                       'id': 'id',
                                       'mac_address': 'mac_address',
                                       'person_id': 'person_id',
                                       'total_bytes': 'total_bytes',
                                       'on_peak': 'on_peak',
                                       'off_peak': 'off_peak'}

        self.person: Dict[str, str] = {'table_name': 'person',
                                       'id': 'id',
                                       'username': 'username',
                                       'on_peak': 'on_peak',
                                       'off_peak': 'off_peak'}

        self.history: Dict[str, str] = {'table_name': 'history',
                                        'id': 'id',
                                        'device_id': 'device_id',
                                        'ip_address': 'ip_address',
                                        'record_time': 'record_time',
                                        'total_bytes': 'total_bytes'}