"""Unit tests"""
import socket
from unittest import TestCase
from mock import Mock

import mytsgraph

class MonitoringTest(TestCase):
    """Unit tests"""

    def test_metrics_slug_format(self):
        """Test slug are well sent"""

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.send = Mock()

        stats = [
            ['TABLE_SCHEMA', 'TABLE_NAME', 10, 20, 30, 40],
        ]

        mytsgraph.loop_to_statsd(sock, stats, 'test', 'dummy')

        for slug in ['test.TABLE_SCHEMA.TABLE_NAME.data_length:10|g',
                     'test.TABLE_SCHEMA.TABLE_NAME.index_length:20|g',
                     'test.TABLE_SCHEMA.TABLE_NAME.data_free:30|g',
                     'test.TABLE_SCHEMA.TABLE_NAME.row_count:40|g',
                    ]:
            sock.send.assert_any_call(slug)

    def test_exclude_databases(self):
        """Test db exclusion"""

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.send = Mock()

        stats = [
            ['remove_me', 'remove_me', 10, 20, 30, 40],
        ]

        mytsgraph.loop_to_statsd(sock, stats, 'test', 'test,remove_me,test2')
        sock.send.assert_not_called()

if __name__ == '__main__':
    unittest.main()
