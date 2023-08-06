"""
Initializes the database with a Wikilabels schema.

Usage:
    load_schema -h | --help
    load_schema [--config=<path>] [--reload-test-data]

Options:
    -h --help           Prints this documentation
    --config=<path>     Path to a config directory to use when connecting
                        to the database [default: config/]
    --reload-test-data  Clears current data and loads test data into the
                        database if set.  This is useful for the dev_server.
"""
import glob
import logging
import os
import sys
from distutils.util import strtobool

import docopt
import yamlconf

from ..database import DB

logger = logging.getLogger(__name__)


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)
    # This expects the database config file path

    config_paths = os.path.join(args['--config'], "*.yaml")
    config = yamlconf.load(*(open(p) for p in sorted(glob.glob(config_paths))))

    db = DB.from_config(config)
    reload_test_data = args['--reload-test-data']

    run(db, reload_test_data)


def run(db, reload_test_data):
    logging.basicConfig(level=logging.INFO)

    directory = os.path.dirname(os.path.realpath(__file__))

    schema_sql = open(os.path.join(directory, "../database/schema.sql")).read()

    logger.info("Loading schema...")
    db.execute(schema_sql)

    if reload_test_data:
        logger.info("Loading test data...")
        if prompt("This will clear the database and reload it with test " +
                  "data. Continue?", default=False):
            path = "../database/schema-testdata.sql"
            test_data_sql = open(os.path.join(directory, path)).read()
            db.execute(test_data_sql)
        else:
            logger.info("Skipped loading test data.")


def prompt(question, default=None):
    if default is None:
        options = " [y/n] "
    elif default:
        options = " [Y/n] "
    else:
        options = " [y/N] "

    while True:
        sys.stdout.write(question + options)
        try:
            val = input().lower().strip()
            if val == "" and default is not None:
                return default
            else:
                return bool(strtobool(val))
        except ValueError as e:
            print(e)
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').")
