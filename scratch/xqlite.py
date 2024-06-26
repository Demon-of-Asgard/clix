import sqlite3 as sql
import feedparser as xmlparser
from typing import List, Dict, Tuple


#---------------------------------------------------------------------------
def create_table(connection, table_name:str=..., schema:Dict=...)->None:
    qstr = f"CREATE TABLE IF NOT EXISTS {table_name} ("
    for key, values in schema.items():
        if key != "info":
            qstr += f"{key} " + " ".join([v for v in values]) + ", "
    if "info" in schema.keys():
        qstr += schema["info"]
    qstr = qstr[:-1].strip(",") + " )"
    print(qstr)
    connection.execute(qstr)
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
def add_relational_data(connection, table:str, relation:str, data:List | Tuple | str)->None:

    return

#---------------------------------------------------------------------------
def sql_entry():
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
    
    with sql.connect("arxiv.db") as connection:

        entries_schema = {
            "article_id" : ("INTEGER", "PRIMARY KEY"),
            "ver" : ("INTEGER", "NOT NULL"),
            "title" : ("TEXT", "NOT NULL"),
            "summary" : ("TEXT", "NOT NULL"),
            "link" : ("TEXT", "NOT NULL")
        }

        author_shema = {
            "name" : ("TEXT", "PRIMARY KEY"),
        }

        relation_shema = {
            "author_name" : ("TEXT",),
            "article_id" : ("INTEGER",),
            "info" : "FOREIGN KEY (author_name) REFERENCES authors (name), FOREIGN KEY(article_id) REFERENCES articles(ROWID) "
        }
       
        create_table(connection=connection, table_name="articles" , schema=entries_schema)
        create_table(connection=connection, table_name="authors", schema=author_shema)
        create_table(connection=connection, table_name="araurel", schema=relation_shema)



        parsed_data = xmlparser.parse(data)
        for entry in parsed_data["entries"][:]:
            title = " ".join(entry['title'].split("\n"))
            summary = entry["summary"]
            xid = entry["link"].split('/')[-1].split('v')[0].split(".")
            article_id = int(xid[0] + xid[1])
            version = int(entry['link'].split('/')[-1].split('v')[1]) if len(entry["link"].split('/')[-1].split('v')) > 1 else None
            meta_link = f"http://arxiv.org/abs/{xid}{version}"
            pdf_link = f"http://arxiv.org/pdf/{xid}{version}"
            link = entry["link"]
            article_meta = (
                    article_id,
                    version, 
                    title, 
                    summary,
                    link, 
                )
            authors = [[e["name"]] for e in entry["authors"]]
            add_item(
                connection=connection,
                table_name="articles",
                field_names=("article_id", "ver", "title", "summary", "link"),
                items=article_meta
            )
            add_items(
                connection=connection, 
                table_name="authors", 
                field_names="name", 
                items=authors
            )
            print("done")
            for author in authors:
                author = "".join(author[0].split("'"))
                qstring = f"""INSERT INTO araurel (author_name, article_id) SELECT '{author}', {article_id} WHERE NOT EXISTS (SELECT 1 FROM araurel WHERE article_id = {article_id} AND author_name = '{author}')"""
                print(qstring)
                connection.execute(
                    qstring
                )

    return

#---------------------------------------------------------------------------
if __name__ == "__main__":
    main()

#---------------------------------------------------------------------------
    