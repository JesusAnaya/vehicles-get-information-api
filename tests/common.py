from sqlalchemy import orm

#
# This session is used for testing. It is created in this module
# so that it can be shared by all tests and the factories.
#
SessionForTesting = orm.scoped_session(
    orm.sessionmaker(autocommit=False, autoflush=False)
)
