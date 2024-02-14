import os
import sqlite3 as sqlt
from datetime import datetime
from typing import List, Dict, Tuple

from utils import Paths, Fields

#---------------------------------------------------------------------------
def create_table(connection, table_name:str=..., schema:Dict=...)->None:
    qstr = f"CREATE TABLE IF NOT EXISTS {table_name} ("
    for key, values in schema.items():
        if key != "info":
            qstr += f"{key} " + " ".join([v for v in values]) + ", "
    if "info" in schema.keys():
        qstr += schema["info"]
    qstr = qstr[:-1].strip(",") + " )"
    stat = connection.execute(qstr)
    return 

#---------------------------------------------------------------------------
def add_items(connection, table_name:str=None, field_names:List | Tuple | str=..., items:List=None)->None:
    items = items if not items == None else []
    assert type(field_names) is list or type(field_names) is tuple or type(field_names) is str, f"""Field names can only be list or tuple. Currently passed 
        objest has type {type(field_names)}"""
    

    if type(field_names) is not str:
        field_names = tuple(field_names)
        place_holders = "(" + ", ".join(["?" for _ in field_names]) + ")"
    else:
        place_holders = "(?)"
        field_names = f"({field_names})"
    qstr = f"INSERT OR IGNORE INTO {table_name} {field_names} VALUES {place_holders}" 
    
    try:
        connection.executemany(qstr, items)
        connection.commit()
    except Exception as e:
        print(f"sqlite3.OperationalError: {e.args}")
    return 

#---------------------------------------------------------------------------

def add_item(connection, table_name:str=None, field_names:List | Tuple | str=..., items:List=None)->None:
    items = items if not items == None else []
    assert type(field_names) is list or type(field_names) is tuple or type(field_names) is str, f"""Field names can only be list or tuple. Currently passed 
        objest has type {type(field_names)}"""
    

    if type(field_names) is not str:
        field_names = tuple(field_names)
        place_holders = "(" + ", ".join(["?" for _ in field_names]) + ")"
    else:
        place_holders = "(?)"
        field_names = f"({field_names})"
    qstr = f"INSERT OR IGNORE INTO {table_name} {field_names} VALUES {place_holders}" 
    
    try:
        connection.execute(qstr, items)
        connection.commit()
    except Exception as e:
        print(f"sqlite3.OperationalError: {e.args}")
    return 

#---------------------------------------------------------------------------
def add_to_db(parsed_data:List|Dict, category:str, identifier:str):
    with sqlt.connect (os.path.join(Paths.DB, f"{identifier}.db")) as connection:
        fields_schema = {
            "id" : ("INTEGER", "PRIMARY KEY"),
            "identifier":("TEXT", ),
        }

        articles_schema = {
            "article_id" : ("INTEGER", "PRIMARY KEY"),
            "ver" : ("INTEGER", "NOT NULL"),
            "date" : ("DATETIME", ),
            "primary_category" : ("TEXT",),
            "title" : ("TEXT", "NOT NULL"),
            "summary" : ("TEXT", "NOT NULL"),
            "link" : ("TEXT", "NOT NULL"),
        }

        author_shema = {
            "name" : ("TEXT", "PRIMARY KEY"),
        }

        relation_shema = {
            "author_name" : ("TEXT",),
            "article_id" : ("INTEGER",),
            "info" : ("FOREIGN KEY (author_name) REFERENCES authors (name),"+ 
                      "FOREIGN KEY(article_id) REFERENCES articles(ROWID) ")
        }


        create_table(connection=connection, table_name="fields" , schema=fields_schema)
        create_table(connection=connection, table_name="articles" , schema=articles_schema)
        create_table(connection=connection, table_name="authors", schema=author_shema)
        create_table(connection=connection, table_name="relate_author_article", schema=relation_shema)

        for entry in parsed_data[:]:
            title = " ".join(entry['title'].split("\n"))
            summary = entry["summary"]
            xid = "".join(entry["link"].split('/')[-1].split('v')[0].split("."))
            article_id = int(xid)
            version = int(entry['link'].split('/')[-1].split('v')[1]) if len(entry["link"].split('/')[-1].split('v')) > 1 else None
            date = datetime.strptime(entry["updated"].split("T")[0], '%Y-%m-%d').date()
            link = entry["link"]
            article_meta = (
                    article_id,
                    version, 
                    date,
                    title, 
                    summary,
                    link, 
                )
            authors = [[e["name"]] for e in entry["authors"]]
            add_item(
                connection=connection,
                table_name="articles",
                field_names=("article_id", "ver", "date", "title", "summary", "link"),
                items=article_meta
            )
            add_items(
                connection=connection, 
                table_name="authors", 
                field_names="name", 
                items=authors
            )
            for author in authors:
                author = "".join(author[0].split("'"))
                qstring = (
                    f"INSERT INTO relate_author_article (author_name, article_id) SELECT '{author}', {article_id} " + 
                    f"WHERE NOT EXISTS " + 
                    f"(SELECT 1 FROM relate_author_article WHERE article_id = {article_id} AND author_name = '{author}')"
                )
                connection.execute(
                    qstring
                )

    return
