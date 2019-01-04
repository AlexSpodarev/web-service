#!/usr/bin/env python
from flask import Flask, request, render_template, abort, jsonify
import sqlite3

app = Flask(__name__)
DB_SIZE = 6


@app.route('/')
def index(template='index.html'):
    return render_template(template)


@app.route('/api/<data>', methods=['POST'])
def api_post(data):
    """
    When the request method is an HTTP/POST, the logic is to grab the data
    Check if it's in the DB, if it's not, we append it to the DB
    """
    input_params = request.get_json()
    if len(input_params) is not (DB_SIZE - 1):
        return reject_invalid_request(422)

    else:
        if content_in_db(data, input_params):
            return "Entry already exist in DB, skipped"
        else:
            return append_to_db(data, input_params)


@app.route('/api/<data>', methods=['GET'])
def api_get(data):
    """
    If the content exist in the DB, fetch it from the DB and return to user, else reject (404)
    """
    if is_in_db(data):
        return fetch_from_db(key=data, request_dict=request.args.to_dict())

    else:
        reject_invalid_request()


def append_to_db(key=None, request_dict=None):
    """
    The variable content starts as None which is the recommended way according to google code style.
    if content is None, a log message is printed with the content and type(content)
    The parameters db and db_mode are initialized to database.csv and a (append) respectively,
    this means this function is universal and the db/db_mode can be changed when calling the function
    Example: append_to_db(content='some content: some value', db='new_db.csv', db_mode='w')
    """
    app.logger.info("Inside the function: append_to_db()")

    if not key and request_dict:
        reject_invalid_request(422)

    else:
        db = open_db_connection()
        cursor = db.cursor()

        param = f' \'{key}\' '
        for k, v in request_dict.items():
            param += f",'{v}'"

        app.logger.info(f"Attempting to append content={key}, type:{type(key)}")
        query = f"INSERT INTO cars(Vendor, Model, Year, Engine, HP, Torque)\
                        VALUES ({param});"

        """Adding content """
        cursor.execute(query)

        """Closing DB"""
        db.commit()

        app.logger.info(f"Successfully appended content={param}, type:{type(param)}")
        return f"Successfully appended content={param}, type:{type(param)}"


def content_in_db(key=None, request_dict=None):
    app.logger.info("Inside the function: content_in_db()")

    if key is not None:

        db = open_db_connection()
        params_list = []
        for k, v in request_dict.items():
            result = f"{k} == '{v}'"
            app.logger.debug(f'{k} == {v}')
            params_list.append(result)
        params = " AND ".join(params_list)

        query = f"SELECT * FROM cars WHERE Vendor == '{key}' AND {params};"
        cursor = db.cursor()

        cursor.execute(query)
        for Vendor, Model, Year, Engine, HP, Torque in cursor.execute(query):
            db_data = {
                'model': str(Model), 'year': str(Year), 'engine': str(Engine), 'HP': str(HP), 'Torque': str(Torque)
            }

            if db_data == request_dict:
                return True
            else:
                return False

    else:
        return reject_invalid_request(422)


def is_in_db(content=None):
    app.logger.info("Inside the function: is_in_db()")

    db = open_db_connection()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM cars WHERE vendor == '{content}';")

    return cursor.fetchall()


def fetch_from_db(key=None, request_dict=None):
    """
    We pass in a key which starts out as None for error handling
    the key is the Vendor of the car, we then open the DB
    and check if the key matches the vendor column, if it does
    we format the string and return it to the function which called
    """
    app.logger.info("Inside the function: fetch_from_db()")

    if key is not None:

        db = open_db_connection()

        params_list = []
        for k, v in request_dict.items():
            if v.isalpha():
                result = f"{k.capitalize()} LIKE '%{v}%'"
            else:
                result = f"{k.capitalize()} == {v}"
            params_list.append(result)
        params = " AND ".join(params_list)

        if not request_dict:
            query = f"SELECT * FROM cars WHERE Vendor == '{key}';"
        else:
            query = f"SELECT * FROM cars WHERE Vendor == '{key}' AND {params};"
        app.logger.debug(query)

        cursor = db.cursor()

        output = []
        for Vendor, Model, Year, Engine, HP, Torque in cursor.execute(query):
            output.append(
                {
                    'Vendor': Vendor.capitalize(),
                    'Model': Model.capitalize(),
                    'Year': Year,
                    'Engine': Engine,
                    'HP': HP,
                    'Torque': Torque
                }
            )

        return jsonify(output)

    else:
        """
        If we didn't get a key, reject the request with a 404 not found
        """
        reject_invalid_request()


def reject_invalid_request(code=404):
    """
    This function is designed to reduce the lines of logic in the routes by 
    Having a generic method to abort requests, when needed, just call reject_invalid_request
    A log message will be printed and the request rejected with a 404 not found by default
    Can be changed by calling the function with a different code example: reject_invalid_request(500)
    """
    app.logger.info(f"Invalid Request:{request} - Dropping with code: {code}")
    abort(code)


def open_db_connection(db='cars.db'):
    conn = sqlite3.connect(db)
    return conn


if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000", debug=True)
