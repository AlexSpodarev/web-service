#!/usr/bin/env python
from flask import Flask
from flask import request
from flask import render_template
from flask import abort

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', name='Alex')


@app.route('/<param>', methods=['GET', 'POST'])
def test(param):
    if request.method == 'GET':
        return f'You have requested {param}'

    elif request.method == 'POST':
        return f'You have posted {param}'


@app.route('/admin')
def reject():
    abort(500)


@app.route('/api/<data>', methods=['POST', 'GET'])
def api(data):
    # ! Code for POST method #########################################
    if request.method == 'POST':
        json = request.get_json()
        exist_in_db_flag = 0
        for words in json:
            entry = (data + "," + json[words] + "\n")

        with open('database.csv', 'r') as f:
            for line in f.readlines():
                if line != '\n':
                    # Checking if the received JSON content already exist in one of the rows of DB.(Flag)
                    if line == entry:
                        exist_in_db_flag = 1
                        app.logger.info("The entry already exist, skipped")
        # Now if the JSON is not in DB - we are writing/appending the row to the DB
        if not exist_in_db_flag:
            with open('database.csv', 'a') as f:
                f.write(entry)
                return f'<h1>Successfully saved to database: {entry}</h1>'
        else:
                return f'<h1>This entry already exist</h1>'

    # ! Code for GET method ##########################################
    elif request.method == 'GET':
        with open('database.csv', 'r') as f:
            result = []
            for line in f.readlines():
                if line != '\n':
                    parsed = line.split(',')
                    vendor = parsed[0].split()[0]
                    model  = parsed[1].split()[0]
                    if data == vendor:
                        our_new_row_is = vendor + " " + model + '\n'
                        result.append(our_new_row_is)

                        app.logger.debug("RESULT is:        %s" % result)
                        app.logger.debug("Adding this line: %s" % our_new_row_is)
                else:
                    abort(404)
            app.logger.debug("Almost final RESULT is: %s" % result)
            result.insert(0, f'<h1>Found entries: {len(result)}</h1>')
            app.logger.debug("       Final RESULT is: %s" % result)
            app.logger.debug("   LENGTH of RESULT is: %s" % len(result))

            return """
                    f'<h1>Found: {result}</h1>'
                    
                    """

    # !  Code if not supported method #################################
    else:
        return f'<h1>ERROR! Current request type isn\'t supported</h1>'


# ! Validation for INPUT messages like POST,PUT etc
def content_validation(content):
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

# @app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
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
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})


if __name__ == '__main__':
    app.run(host='192.168.14.93', port="5000", debug=True)
