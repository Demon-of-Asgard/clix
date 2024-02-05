import sqlite3 as sql
import feedparser as xmlparser
from typing import List, Dict, Tuple


#---------------------------------------------------------------------------
def create_table(connection, table_name:str=..., schema:Dict=...)->None:
    qstr = f"CREATE TABLE IF NOT EXISTS {table_name} ("
    for key, values in schema.items():
        qstr += f"{key} " + " ".join([v for v in values]) + ", "
    qstr = qstr[:-2] + " )"
    print(qstr)
    connection.execute(qstr)
    return


#---------------------------------------------------------------------------
def add_items(connection, table_name:str=None, field_names:List | Tuple=..., items:List=None)->None:
    items = items if not items == None else []
    assert type(field_names) is list or type(field_names) is tuple, f"""Field names can only be list or tuple. Currently passed 
        objest has type {type(field_names)}"""
    field_names = tuple(field_names)
    assert field_names is not None, "Field names can only be "
    place_holders = "(" + ", ".join(["?" for _ in field_names]) + ")"
    qstr = f"INSERT OR IGNORE INTO {table_name} {field_names} VALUES {place_holders}" 
    try:
        connection.execute(qstr, items)
        connection.commit()
    except Exception as e:
        print(f"sqlite3.OperationalError: {e.args}")
    return 


#---------------------------------------------------------------------------
def sql():
    with sql.connect("xdb.db") as connection:
        schema = {
            "Id" : ("INTEGER", ),
            "Title" : ("TEXT", "PRIMARY KEY"),
            "Author" : ("TEXT", )
        }
        table_name = "preXs"
        create_table(connection=connection, table_name=table_name, schema=schema)
        items = [1, "The Great Gatsby", "F. Scott Fitzgerald"]
        add_items(connection=connection, table_name=table_name, field_names=("id", "Title", "Author"), items=items)

def main()->None:
    with open("test.xml", "r") as f:
        data = f.read()
    
    parsed_data = xmlparser.parse(data)
    print(parsed_data["items"][0]["title"])
    print(parsed_data["items"][0]["summary"])

    return

#---------------------------------------------------------------------------
if __name__ == "__main__":
    main()

#---------------------------------------------------------------------------
    