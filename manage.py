''' Created by Migwi Ndung'u
    @ The Samurai Community 2017
'''
from video_chat_bot import app
from app.models import db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

migrate = Migrate(app, db)
manager = Manager(app)


def db_exist():
    # Command used to check if the tables in the db exist
    engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    user_table = engine.dialect.has_table(engine, 'users')
    transaction_table = engine.dialect.has_table(engine, 'transactions')

    if user_table and transaction_table:
        return False
    return True


if db_exist():
    '''If all the tables exist no migration that should run'''
    manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
