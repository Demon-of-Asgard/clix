import os 
import datetime

from arxiv_api_query import ArXapi
from utils import (Paths, clear, get_shell_text)
#------------------------------------------------------------------------------
def make_query_and_parse(
        category:str=..., identifier:str=..., 
        base_url:str=..., do_reload:bool=False,
    )->list:

    start_index=0
    max_results=100

    query_obj = ArXapi(
        category=category,
        identifier=identifier,
        base_url=base_url,
        reload=do_reload,
    ) 

    today = datetime.datetime.now().date()
    identifier_db_root = os.path.join(Paths.DB, query_obj.identifier)
        
    try:
        if not os.path.exists(identifier_db_root):
            os.makedirs(identifier_db_root)
    except Exception as e:
        print(f"Exeption occures while creating folder "
            + f"{identifier_db_root}. Details:\n\t{e.args}"
        )
        return 

    response = None
    qury_save_file = os.path.join(
        identifier_db_root, 
        f"{today}_{start_index}_{start_index+max_results}.xml"
    )
    if not os.path.exists(qury_save_file) or query_obj.reload:
        if not query_obj.reload:
            print(
                get_shell_text(text="Loading", color="green") 
                + get_shell_text(text="...", color="green", style="blink")
            )
        else:
            print(
                get_shell_text(text="Reloading", color="green") 
                + get_shell_text(text="...", color="green", style="blink")
            )

        query = query_obj.construct_search_query(
            sort_method="submitted_date",
            sort_order="descending",
            start_index=0,
            max_results=100,
        )
        status, response = query_obj.make_query()
        with open(qury_save_file, "wb") as f:
            f.write(response)
    else:
        with open(qury_save_file, "rb") as f:
            response = f.read()
    
    parsed_response = query_obj.parse_response(response=response)
    # query_obj.render_parsed_response()

    return parsed_response
