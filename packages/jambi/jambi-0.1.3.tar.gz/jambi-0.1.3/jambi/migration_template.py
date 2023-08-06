"""
A jambi migration.
"""
from peewee import *


def upgrade(migrator):
    """for more information on migrator commands, see:
    http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#schema-migrations

    Arguments:
    migrator -- a PostgresqlMigrator object that performs migration tasks

    Returns:
    a tuple of migrator schema-altering statements to run for this version
    """
    return (
        # migrator.add_column('table', 'column', CharField(null=True)),
    )
