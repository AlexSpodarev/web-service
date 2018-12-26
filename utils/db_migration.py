"""""
    This function takes the old database.csv file with 2 elements
    and creates a new database with 3 elements. In the end there is
    a validation that every row is taken care properly.
    
    1.Defining PATH and Filename of origin and new DB for future use.
    2.(field_type) variable is the Type of the field we want to add
    as a dimension to our DB.
    Possible values are 'Year', 'Engine', 'HP', 'Torque'
"""""

import os
import random

path_new = 'C:\\Users\\Alex\\PycharmProjects\\web-service\\Utils'
path_old = 'C:\\Users\\Alex\\PycharmProjects\\web-service'
file_new = 'database_new.csv'
file_old = 'database.csv'
db_path_new = f'{path_new}\\{file_new}'
db_path_old = f'{path_old}\\{file_old}'

field_type = 'Year'
origin_fields: int = 2


def main():
    """
        First we validate that Original DB suites expected format.
        Second we extend our new DB from the origin DB.
        Also we validate that amount of lines is the same after conversion.
    """
    format_old = validate_content(db_path_old, origin_fields)

    if format_old:
        print(copy_and_add_content(db_path_old, db_path_new, field_type))

        format_new = validate_content(db_path_new, (origin_fields + 1))

        if (line_amount(db_path_old) != line_amount(db_path_new)) \
                and format_new:
            print(f'ERROR: Hewstone, we have a problem!')
        else:
            print(f'SUCCESS: DB migration passed successfully.')

    else:
        print(f'ERROR: DB migration failed!')

#   file_deletion(db_path_new, file_new)
"""
    Helper functions to operate on the db files.
"""

def copy_and_add_content(path_old, path_new, new_field_type):
    """
        This function takes old DB file and creates new DB file with extensions.
        First raw is the Title of each column, additional Title field added.
        New column values are filled according to the field_type with realistic values.
    """
    old = open(path_old, "r")
    line = old.readline()
    item = line.split("\n")[0]
    row = f"{item},{new_field_type}\n"

    for line in old:
        line = line.split("\n")[0]
        if new_field_type == 'Year':
            row += f'{line},{random.randint(2001, 2019)}\n'
        elif new_field_type == 'Engine':
            row += f'{line},{random.randrange(1200, 2000, 200)}\n'
        elif new_field_type == 'HP':
            row += f'{line},{random.randrange(120, 420, 50)}\n'
        elif new_field_type == 'Torque':
            row += f'{line},{random.randrange(250, 500, 50)}\n'
    old.close()

    with open(path_new, "w") as new:
        new.write(row)

    return (f'SUCCESS: DB is extended.')


def validate_content(db_path, fields):
    flag = 0
    with open(db_path, "r") as f:
        for line in f:
            line = line.split(",")
            if len(line) != fields:
                print(f'ERROR: in row {line} the num. of fields: {len(line)}')
                flag = 1

    if flag == 0:
        print(f'The database has correct number of fields: {fields}')
        return True
    else:
        print(f'Number of fields doesn\'t match: {fields}')
        return False


def file_deletion(db_path, filename):
    os.remove(db_path)
    return f'File {filename} removed successfully'


def line_amount(db_path):
    count = 0
    with open(db_path, "r") as f:
        for line in f:
            count += 1
    return count

if __name__ == "__main__":
    main()
