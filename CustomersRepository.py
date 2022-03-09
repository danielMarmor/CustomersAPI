from LoggingService import CustomersLogger
import logging


class CustomersRepository:
    def __init__(self, local_session):
        self.local_session = local_session
        self.logger = CustomersLogger.get_instance().Logger

    def execute_script(self, text_command):
        try:
            self.local_session.execute(text_command)
            self.logger.log(logging.INFO, f'execute_script')
        except Exception as ex:
            self.logger.log(logging.ERROR, f'execute_script: {str(ex)}')
            raise ex

        # reset_table_auto_incerement
    def reset_table_auto_incerement(self, table_class):
        try:
            self.local_session.execute(f'TRUNCATE TABLE {table_class.__tablename__} RESTART IDENTITY CASCADE')
            # SUCCEDED
            self.logger.log(logging.INFO, f'reset_table_auto_incerement: {table_class.__tablename__}')
        except Exception as ex:
            self.logger.log(logging.ERROR, f'reset_table_auto_incerement: {str(ex)}')
            raise ex

    # get_by_id
    def get_by_id(self, table_class, entry_id):
        try:
            entry = self.local_session.query(table_class).get(entry_id)
            # SUCCEDED
            self.logger.log(logging.INFO, f'get_by_id: {str(entry)}')
            return entry
        except Exception as ex:
            self.logger.log(logging.ERROR, f'get_by_id: {str(ex)}')
            raise ex

    # get all
    def get_all(self, table_class):
        try:
            entries = self.local_session.query(table_class).all()
            # SUCCEDED
            self.logger.log(logging.INFO, f'get_all: {str(entries)}')
            return entries
        except Exception as ex:
            self.logger.log(logging.ERROR, f'get_all: {str(ex)}')
            raise ex

    # add
    def add(self, entry):
        try:
            self.local_session.add(entry)
            self.local_session.commit()
            # SECCEDED
            self.logger.log(logging.INFO, f'add: {str(entry)}')
        except Exception as ex:
            self.logger.log(logging.ERROR, f'add: {str(ex)}')
            raise ex

    # update
    def update(self, table_class, id_column_name, entry_id, data):
        try:
            entry = self.local_session.query(table_class).filter(getattr(table_class, id_column_name) == entry_id)
            entry.update(data)
            self.local_session.commit()
            # SECCEDED
            self.logger.log(logging.INFO, f'update: {table_class}, {entry_id}, {str(data)}')
        except Exception as ex:
            self.logger.log(logging.ERROR, f'update: {str(ex)}')
            raise ex

    # delete
    def remove(self, table_class, id_column_name, entry_id):
        try:
            entry = self.local_session.query(table_class).filter(getattr(table_class, id_column_name) == entry_id)
            entry.delete(synchronize_session=False)
            self.local_session.commit()
            # SECCEDED
            self.logger.log(logging.INFO, f'remove: {entry}')
        except Exception as ex:
            self.logger.log(logging.ERROR, f'remove: {str(ex)}')
            raise ex

    def get_all_by_condition(self, table_class, condition):
        try:
            query = self.local_session.query(table_class)
            entries = condition(query).all()
            # SECCEDED
            self.logger.log(logging.INFO, f'get_all_by_condition: {str(entries)}')
            return entries
        except Exception as ex:
            self.logger.log(logging.ERROR, f'get_all_by_condition: {str(ex)}')
            raise ex

