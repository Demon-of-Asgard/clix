import os
import sys
import datetime
from arxiv_api_query import ArXapi
from utils import (Cmd, Os, Paths, ArXurls, clear, get_shell_text)


#------------------------------------------------------------------------------
def render_cat_and_subcat(
        category_info:dict, category_list:list, sub_category_list:list,
        id_current_cat:int=0, id_current_subcat:int=0, 
        key_buffer:list=[], buffermode_on:bool=False
    )->None:

    clear()
    # Render categories and sub-categories
    for i, cat in enumerate(category_list):
        current_sub_cats = sub_category_list[i]
        if i == id_current_cat:
            print(f"[{i}] " + get_shell_text(
                text=cat, color='grey', style='bg'))
            
            for j, sub_cat in enumerate(current_sub_cats):
                if id_current_subcat >= len(current_sub_cats):
                    id_current_subcat = 0
                if id_current_subcat < 0:
                    id_current_subcat = len(current_sub_cats) -1 
                if j == id_current_subcat:
                    print("\t" + get_shell_text(
                        text=f'[{j}] {category_info[cat][sub_cat]}', 
                        color='green'))
                else:
                    print(f"\t[{j}] {category_info[cat][sub_cat]}")
        else:
            print(f"[{i}] {cat}")

    if buffermode_on:
        print(f"{''.join(key_buffer)}", end=' \b')
        sys.stdout.flush()
    
    return None


#------------------------------------------------------------------------------
def manage_and_render_query_and_selection(
        category:str=..., identifier:str=..., 
        base_url:str=..., do_reload:bool=False,
    )->None:

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
    query_obj.render_parsed_response()

    return None


#------------------------------------------------------------------------------
def render_parsed_response(pasrsed_response:list=...)->None:
    pass
