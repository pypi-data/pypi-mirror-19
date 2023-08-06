#!/usr/bin/env python

import argparse
import logging
import os
import sys

import sqlalchemy

from .metrics import optityper_result

def get_param(args, param_name):
    if vars(args)[param_name] == None:
        return None
    else:
        return vars(args)[param_name]
    return

def setup_logging(tool_name, args, uuid):
    logging.basicConfig(
        filename=os.path.join(uuid + '_' + tool_name + '.log'),
        level=args.level,
        filemode='w',
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d_%H:%M:%S_%Z',
    )
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    logger = logging.getLogger(__name__)
    return logger

def main():
    parser = argparse.ArgumentParser('picard docker tool')

    # Logging flags.
    parser.add_argument('-d', '--debug',
        action = 'store_const',
        const = logging.DEBUG,
        dest = 'level',
        help = 'Enable debug logging.',
    )
    parser.set_defaults(level = logging.INFO)

    # Required flags.
    parser.add_argument('--metric_path',
                        required = False
    )
    parser.add_argument('--uuid',
                        required = True,
                        help = 'uuid string',
    )

    # setup required parameters
    args = parser.parse_args()
    metric_path = args.metric_path
    uuid = args.uuid

    logger = setup_logging('optityper_result', args, uuid)

    sqlite_name = uuid + '.db'
    engine_path = 'sqlite:///' + sqlite_name
    engine = sqlalchemy.create_engine(engine_path, isolation_level='SERIALIZABLE')

    optityper_result.run(uuid, metric_path, engine, logger)

    return

if __name__ == '__main__':
    main()
