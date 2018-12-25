#!/usr/bin/env python
from flask import Flask
from flask import request
from flask import render_template
from flask import abort

app = Flask(__name__)


@app.route('/')
def index(template='index.html', name='Alex'):
    return render_template(template, name)


@app.route('/admin')
def reject():
    reject_invalid_request(500)


@app.route('/api/<data>', methods=['POST', 'GET'])
def api(data):
    """
    This route is designed to handle api requests coming to the ur <server>/api/param
    where param is a car Vendor, example: <server>/api/seat
    """
    if request.method == 'POST':
        """
        When the request method is an HTTP/POST, the logic is to grab the data
        Check if it's in the DB, if it's not, we append it to the DB
        TODO: Duplicates/Case/Error handling should be added
        """
        json = request.get_json()

        for words in json:
            entry = f"{data},{json[words]}\n"

        if content_in_db(entry):
            return f'<h1>This Entry Already Exist</h1>'

        else:
            append_to_db(entry)
            return f'<h1>Successfully saved {entry}</h1>'

    elif request.method == 'GET':
        """
        Logic for HTTP/GET
        If the content exists in the DB, fetch it from the DB and return to user
        """
        if content_in_db(data):
            reply = fetch_from_db(data)
            return f'<h1>Found: {reply}</h1>'

        else:
            reject_invalid_request()

        app.logger.debug(f"[DEBUGGING]: Final RESULT is: {result}")
        app.logger.debug(f"[DEBUGGING]: Le of RESULT is: {len(result)}")
        result.insert(0, f'<h1>Found entries: {len(result)}</h1>')

    else:
        """
        If method is not implemented reject with code 500 - (Internal Server Error)
        """
        reject_invalid_request(500)


def content_validation(content):
    """
    This function is used when validation of input is needed in 
    HTTP methods which results in writing to us (server)
    """
    if not request.json or 'title' not in request.json:
        reject_invalid_request(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get(
        'description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})


def append_to_db(content=None, db='database.csv', db_mode='a'):
    """
    The variable content starts as None which is the recommended way according to google code style.
    if content is None, a log message is printed with the content and type(content)
    The parameters db and db_mode are initialized to database.csv and a (append) respectivly,
    this means this function is universable and the db/db_mode can be changed when calling the function
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

                if line.split(',')[0].split()[0] == content:
                    """
                    This chunk of code has the logic to check if the data recieved 
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


def fetch_from_db(key=None, db='database.csv', db_mode='r'):
    """
    We pass in a key which starts out as None for error handling
    the key is the Vendor of the car, we then open the DB
    and check if the key matches the vendor column, if it does
    we format the string and return it to the function which called
    """
    if key is not None:

        with open(db, db_mode) as f:
            for line in f.readlines():

                if line != '\n':
                    parsed = line.split(',')
                    vendor = parsed[0].split()[0]
                    model = parsed[1].split()[0]

                    if vendor == key:
                        """
                        Those are strings so I can use .capitalize to make the first
                        Letter an uppercase, ex: seat leon -> Seat Leon
                        """
                        return f'{vendor.capitalize()} {model.capitalize()}'

                else:
                    """
                    If for some reason we reached the end of the file 
                    and we can't find the key in the database we reject the request
                    Code 501 - Internal Server Error
                    """
                    reject_invalid_request(501)

    else:
        """
        If we didn't get a key reject the request with a 404 not found
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


if __name__ == '__main__':
    """
    If we hardcode the IP address of the host it will not run out of the box on new installations
    Changing this to 0.0.0.0 to listen on all interfaces
    """
    app.run(host='0.0.0.0', port="5000", debug=True)
