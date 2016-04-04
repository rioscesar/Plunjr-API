import csv
import os

from sqlalchemy.exc import SQLAlchemyError

from flaskapp import db
from flaskapp.main.models import Review, Restroom


def recreate_db():
    try:
        db.reflect()
        db.drop_all()
    except SQLAlchemyError as e:
        raise ValueError(e)

    db.create_all()

    db.session.commit()


def _map_csv_to_list_of_dicts(filename):
    current_path = os.path.dirname(__file__)
    csv_path = os.path.join(current_path, 'db_setup', filename)

    dicts = []

    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        column_headers = []
        for row in reader:
            if len(column_headers) is 0:
                column_headers = row
            else:
                col_num = 0
                csv_row_as_dict = {}
                for column_header in column_headers:
                    try:
                        csv_row_as_dict[column_header] = row[col_num]
                    except IndexError as e:
                        pass
                    col_num += 1

                dicts.append(csv_row_as_dict)

    return dicts


def _map_dict_to_object(dict_to_map, obj):
    for key in dict_to_map:
        value = dict_to_map[key]
        if value is not None and value != '':
            setattr(obj, key, dict_to_map[key])


def _seed_csv_reviews():
    csv_filename = 'seed_data/reviews.csv'
    dicts = _map_csv_to_list_of_dicts(csv_filename)

    for review_dict in dicts:
        review = Review()
        _map_dict_to_object(review_dict, review)
        db.session.add(review)


def _seed_csv_restrooms():
    csv_filename = 'seed_data/restrooms.csv'
    dicts = _map_csv_to_list_of_dicts(csv_filename)

    for restroom_dict in dicts:
        restroom = Restroom()
        _map_dict_to_object(restroom_dict, restroom)
        db.session.add(restroom)


def reset_postgres_id_sequences():
    tables = ['reviews', 'restrooms']

    for table in tables:
        sql = "SELECT setval('{0}_id_seq', MAX(id)) FROM {0};".format(table)
        db.engine.execute(sql)


def seed_data():
    # recreate_db()
    _seed_csv_reviews()
    _seed_csv_restrooms()

    # reset_postgres_id_sequences()

    db.session.commit()
