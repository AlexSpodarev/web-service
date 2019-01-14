from cars_api import app
from cars_api.errors import reject_invalid_request
import sqlite3


def is_in_db(content=None, db=None):
    """
     +------------------------------------------------------------------------------------------------------------------
     | This function verifies if the specific Vendor name exist inside DB before that we run complicated logic
     +------------------------------------------------------------------------------------------------------------------
     """
    if (db is not None) and (content is not None):
        app.logger.info("Inside the function: is_in_db()")
        cursor = db.cursor()
        return cursor.execute(f"SELECT * FROM cars WHERE Vendor like '%{content}%';").fetchall()

    else:
        reject_invalid_request()


def fetch_from_db(key=None, request_dict=None, db=None):
    """
    +-------------------------------------------------------------------------------------------------------------------
    | Function searches for the entry that we want to GET, when match - we format and return
    +-------------------------------------------------------------------------------------------------------------------
    """
    app.logger.info("Inside the function: fetch_from_db()")

    if key and db:

        params_list = []

        for k, v in request_dict.items():
            result = f"{k.capitalize()} LIKE '%{v}%'" if v.isalpha() else f"{k.capitalize()} == {v}"
            params_list.append(result)

        params = " AND ".join(params_list)

        """ Query can be done on short URL or URL with args """
        if not request_dict:
            query = f"SELECT * FROM cars WHERE Vendor == '{key}';"

        else:
            query = f"SELECT * FROM cars WHERE Vendor == '{key}' AND {params};"

        # DEBUGGING: PRINT OUT THE QUERY TO BE USED
        app.logger.debug(query)

        output = []
        for Id, Vendor, Model, Year, Engine, HP, Torque in db.cursor().execute(query):
            output.append(
                {
                    'Id': Id,
                    'Vendor': Vendor.capitalize(),
                    'Model': Model.capitalize(),
                    'Year': Year,
                    'Engine': Engine,
                    'HP': HP,
                    'Torque': Torque
                }
            )
        return output

    else:
        """ If we didn't get a key, reject the request with a 404 not found """
        reject_invalid_request()


def append_to_db(key=None, request_dict=None, db=None):
    """
    +-------------------------------------------------------------------------------------------------------------------
    | The variable content starts as None which is the recommended way according to google code style.
    | if content is None, a log message is printed with the content and type(content)
    | Vendor received from URL and other parameters received by JSON
    | Function gathers all the parameters for Car and inserts row into DB
    +-------------------------------------------------------------------------------------------------------------------
    """
    app.logger.info("Inside the function: append_to_db()")

    if not (key or request_dict or db):
        reject_invalid_request(422)

    else:
        """
        Variable "param" gathers all DATA that we want to insert into DB 
        """
        param = f"'{key}'"
        for k, v in request_dict.items():
            param += f",'{v}'"

        app.logger.debug(f"Attempting to append content={key}, type:{type(key)}")

        query = f"INSERT INTO cars(Id, Vendor, Model, Year, Engine, HP, Torque) VALUES ({param});"

        """
        Adding content and committing changes to DB 
        """
        db.cursor().execute(query)
        db.commit()

        app.logger.debug(f"Successfully appended content={param}, type:{type(param)}")

        return f"Successfully appended content={param}, type:{type(param)}"


def content_in_db(key=None, request_dict=None, db=None):
    """
     +------------------------------------------------------------------------------------------------------------------
     | This function verifies if the specific car spec. already inside DB before we want to insert it into DB
     +------------------------------------------------------------------------------------------------------------------
     """
    app.logger.info("Inside the function: content_in_db()")

    if key and db:

        params_list = [f"{k} == '{v}'" for k, v in request_dict.items()]
        params = " AND ".join(params_list)

        query = f"SELECT * FROM cars WHERE Vendor == '{key}' AND {params};"

        for Id, Vendor, Model, Year, Engine, HP, Torque in db.cursor().execute(query):
            db_data = {
                'model': str(Model),
                'year': str(Year),
                'engine': str(Engine),
                'HP': str(HP),
                'Torque': str(Torque)
            }

            """
            First match row in DB we return that entry exist in DB 
            """
            return True if db_data == request_dict else False

    else:
        return reject_invalid_request(422)


def sqlite3_connect(db='cars.db'):
    """
    +-------------------------------------------------------------------------------------------------------------------
    | This function in late release will be removed and SQLITE3 connection will be available from main code
    +-------------------------------------------------------------------------------------------------------------------
    """
    return sqlite3.connect(database=db, check_same_thread=False)


def maximal_database_size(size=6):
    return size - 1
