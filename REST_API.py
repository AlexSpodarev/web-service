#!/usr/bin/env python
from flask import Flask, request, render_template, abort, jsonify

app = Flask(__name__)


@app.route('/')
def index(template='index.html', name='X'):
    return render_template(template, name)


@app.route('/api/<data>', methods=['POST'])
def api_post(data):
    """
    When the request method is an HTTP/POST, the logic is to grab the data
    Check if it's in the DB, if it's not, we append it to the DB
    TODO: Duplicates/Case/Error handling should be added
    """
    if data.split('/')[0].isalpha():

        for words in request.get_json():
            entry = f"{data},{words}\n"
            app.logger.debug(entry)

        if content_in_db(entry):
            return f'<h1>This entry already exist</h1>'

        else:
            append_to_db(entry)
            return f'<h1>Successfully saved {entry}</h1>'
    else:
        app.logger.info('Someone tried to POST non-alpha format')
        reject_invalid_request(406)


@app.route('/api/<data>', methods=['GET'])
def api_get(data):
    """
    Logic for HTTP/GET
    If the content exist in the DB, fetch it from the DB and return to user, else reject (404)
    """
    if is_in_db(data):
        return fetch_from_db(data)

    else:
        reject_invalid_request()


def fetch_from_db(key=None, db='database.csv', db_mode='r'):
    """
    We pass in a key which starts out as None for error handling
    the key is the Vendor of the car, we then open the DB
    and check if the key matches the vendor column, if it does
    we format the string and return it to the function which called
    """

    app.logger.info("Inside the function: fetch_from_db()")
    Somelist = []
    if key is not None:

        with open(db, db_mode) as file:

            for idx, line in enumerate(file.readlines()):
                if idx == 0:
                    header = line.strip().split(',')
                    v1, v2, v3, v4, v5, v6 = header

                elif line != '\n':
                    parsed = line.split(',')
                    vendor = parsed[0].split()[0]
                    model = parsed[1].split()[0]
                    year = parsed[2].split()[0]
                    engine = parsed[3].split()[0]
                    hp = parsed[4].split()[0]
                    torque = parsed[5].split()[0]

                    if vendor == key:
                        Somelist.append(
                            {
                                v1: vendor,
                                v2: model,
                                v3: year,
                                v4: engine,
                                v5: hp,
                                v6: torque
                            }
                        )

                elif line == '\n':
                    """
                    If for some reason we reached the end of the file 
                    and we can't find the key in the database we reject the request
                    Code 501 - Internal Server Error
                    """
                    reject_invalid_request(501)

            return jsonify(Somelist)
    else:
        """
        If we didn't get a key, reject the request with a 404 not found
        """
        reject_invalid_request()


def is_in_db(content=None, db='database.csv', db_mode='r'):
    app.logger.info("Inside the function: is_in_db()")
    result = []
    with open(db, db_mode) as f:
        for line in f.readlines():
            if line != '\n':
                if line.split(',')[0] == content:
                    app.logger.info(f'Exist,appending:{line}')
                    result.append(line)

            else:
                app.logger.info(f"Couldn't find '{content}' in '{db}'")
                return result
        return result


def content_in_db(content=None, db='database.csv', db_mode='r'):
    app.logger.info("Inside the function: content_in_db()")
    with open(db, db_mode) as f:
        """
        Opening the database.csv file and parsing line by line
        if the line doesn't contain only a \n than it has data,
        otherwise we realise that it is the end of the file and don't attempt
        any processing on that line as that will result in an exception.
        TODO: We will wan't to change this to an SQLite DB which is ran locally.
        """
        for line in f.readlines():
            if line != '\n':
                app.logger.info(f"Current Line: {line}")
                app.logger.info(f"Content     : {content}")

                if line == content:
                    """
                    This chunk of code has the logic to check if the data received 
                    In the HTTP/POST already exists in the DB.
                    When the line already exists, exists_in_db is set to 1.
                    which is used later on in this method to determine if further processing
                    should be done (might want to use type:boolean)
                    """
                    app.logger.info("The entry already exist, skipped")
                    return True

            else:
                app.logger.info(f"Couldn't find '{content}' in '{db}'")
                return False


def append_to_db(content=None, db='database.csv', db_mode='a'):
    """
    The variable content starts as None which is the recommended way according to google code style.
    if content is None, a log message is printed with the content and type(content)
    The parameters db and db_mode are initialized to database.csv and a (append) respectively,
    this means this function is universal and the db/db_mode can be changed when calling the function
    Example: append_to_db(content='some content: some value', db='new_db.csv', db_mode='w')
    """
    app.logger.info("Inside the function: append_to_db()")

    if not content:
        app.logger.info(f"Invalid content provided, content={content} type:{type(content)}")
        reject_invalid_request(500)

    else:
        app.logger.info(f"Attempting to append content={content}, type:{type(content)} To: {db}")
        with open(db, db_mode) as f:
            f.write(content)
            app.logger.info(f"Successfully appended content={content}, type:{type(content)} To: {db}")


def reject_invalid_request(code=404):
    """
    This function is designed to reduce the lines of logic in the routes by 
    Having a generic method to abort requests, when needed, just call reject_invalid_request
    A log message will be printed and the request rejected with a 404 not found by default
    Can be changed by calling the function with a different code example: reject_invalid_request(500)
    """
    app.logger.info(f"Invalid Request:{request} - Dropping with code: {code}")
    abort(code)


if __name__ == '__main__':
    """
    If we hardcode the IP address of the host it will not run out of the box on new installations
    Change this to 0.0.0.0 to listen on all interfaces
    """
    app.run(host='0.0.0.0', port="5000", debug=True)
