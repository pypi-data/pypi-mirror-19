"""
This module allows to add some mysql metrics in a graphite database through
statsd.
"""


import ConfigParser
import os.path
import socket

from argparse import ArgumentParser
from MySQLdb import connect


def parse_arguments():
    """Parse arguments."""

    arg_parser = ArgumentParser()
    arg_parser.add_argument('--config', '-c', help="Configuration file",
                            type=file, required=True)
    # Allow "catch all" since we're dealing with simple argument parsing.
    # pylint: disable=broad-except
    try:
        return arg_parser.parse_args()
    except Exception as err:
        print err
        exit(1)

def load_configuration(configuration_file):
    """Load configuration from conf file (ini format)."""

    configuration = ConfigParser.ConfigParser()
    configuration.readfp(configuration_file)
    return configuration

def get_mysql_table_stats(mysql):
    """Query database for statistics."""

    sql = """
SELECT
    TABLE_SCHEMA,
    TABLE_NAME,
    IFNULL(DATA_LENGTH,0),
    IFNULL(INDEX_LENGTH,0),
    IFNULL(DATA_FREE,0),
    IFNULL(TABLE_ROWS, 0)
FROM information_schema.tables
WHERE
    ENGINE = 'innodb'
"""
    cursor = mysql.cursor()
    cursor.execute(sql)

    return cursor.fetchall()

def loop_to_statsd(sock, stats, prefix, excluded_databases):
    """Push statistics to graphite (udp socket to statsd)."""

    excluded = [x.strip() for x in excluded_databases.split(',')]

    for row in stats:
        if row[0] in excluded:
            continue

        metrics = [
            "%s.%s.%s.data_length:%d|g" % (prefix, row[0], row[1], row[2]),
            "%s.%s.%s.index_length:%d|g" % (prefix, row[0], row[1], row[3]),
            "%s.%s.%s.data_free:%d|g" % (prefix, row[0], row[1], row[4]),
            "%s.%s.%s.row_count:%d|g" % (prefix, row[0], row[1], row[5]),
        ]
        for metric in metrics:
            print metric
            sock.send(metric)

def main():
    """Program entry point."""
    args = parse_arguments()
    configuration = load_configuration(args.config)

    #create mysql connection
    mysql = connect(
        host=configuration.get('mysql', 'host'),
        port=configuration.getint('mysql', 'port'),
        user=configuration.get('mysql', 'user'),
        passwd=configuration.get('mysql', 'password'))

    #create statsd connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((configuration.get('statsd', 'host'),
                  configuration.getint('statsd', 'port')))

    stats = get_mysql_table_stats(mysql)
    loop_to_statsd(sock, stats, configuration.get('statsd', 'slug_prefix'),
                   configuration.get('mysql', 'exclude_databases'))

    #Close resources
    mysql.close()
    sock.close()
