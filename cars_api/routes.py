from cars_api import app, dbtools, db, Cars
from cars_api.errors import reject_invalid_request
from flask import request, jsonify


# from cars import Cars, db


@app.route('/api/<data>', methods=['GET'])
def api_get(data):
    """
    +-------------------------------------------------------------------------------------------------------------------
    | If the content exist in the DB, fetch it from the DB and return to user, else reject (404)
    +-------------------------------------------------------------------------------------------------------------------
    """
    request_dict = {
        k.capitalize(): v if v.isalpha() else int(v) for k, v in request.args.items()
    }
    app.logger.info(request_dict)

    for car in Cars.query.filter_by(**request_dict).all():
        app.logger.info(f"{car.Id}, {car.Model}, {car.Year}, {car.Engine}, {car.HP}, {car.Torque}")

    y = Cars.query.filter(Cars.Vendor.contains(data)).first()
    print(f"{y.Id}, {y.Model}, {y.Year}, {y.Engine}, {y.HP}, {y.Torque}")

    """ - Commented out, still not sure on a final solution for this
    Cars.Model.like(f'%{request.args.get("model")}%' if request.args.get("model") else None),
    (Cars.Year == request.args.get("year")) if request.args.get("year") else None,
    Cars.Engine.like(f'%{request.args.get("engine")}%'),
    Cars.HP.like(f'%{request.args.get("hp")}%'),
    Cars.Torque.like(f'%{request.args.get("torque")}%')
    """

    if dbtools.is_in_db(content=data, db=db):
        return jsonify(dbtools.fetch_from_db(key=data, request_dict=request.args.to_dict(), db=db))

    else:
        reject_invalid_request()


@app.route('/api/<data>', methods=['POST'])
def api_post(data):
    """
    +-------------------------------------------------------------------------------------------------------------------
    | When the request method is an HTTP/POST, the logic is to grab the data
    | Check if it's in the DB, if it's not, we append it to the DB
    +-------------------------------------------------------------------------------------------------------------------
    """
    input_params = request.get_json()

    if len(input_params) != dbtools.maximal_database_size():
        return reject_invalid_request(422)

    else:

        if dbtools.content_in_db(key=data, request_dict=input_params, db=db):
            return "Entry already exist in DB, skipped"

        return dbtools.append_to_db(key=data, request_dict=input_params, db=db)
