import os 
import sys
import yaml
import getkey
import pprint 
import datetime
from arxiv_api_query import ArXapi
from utils import (Cmd, Os, Paths, ArXurls, clear, get_shell_text)

def manage_and_render_query_and_selection(category:str=..., identifier:str=..., base_url:str=..., do_reload:bool=False):

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
        print(f"Exeption occures while creating folder {identifier_db_root}. Details:\n\t{e.args}")
        return 

    response = None
    qury_save_file = os.path.join(identifier_db_root, f"{today}_{start_index}_{start_index+max_results}.xml")
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

    return 

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
            print(f"[{i}] {get_shell_text(text=cat, color='grey', style='bg')}")
            for j, sub_cat in enumerate(current_sub_cats):
                if id_current_subcat >= len(current_sub_cats):
                    id_current_subcat = 0
                if id_current_subcat < 0:
                    id_current_subcat = len(current_sub_cats) -1 
                if j == id_current_subcat:
                    print(f"\t{get_shell_text(text=f'[{j}] {category_info[cat][sub_cat]}', color='green')}")
                else:
                    print(f"\t[{j}] {category_info[cat][sub_cat]}")
        else:
            print(f"[{i}] {cat}")

    if buffermode_on:
        print(f"{''.join(key_buffer)}", end=' \b')
        sys.stdout.flush()
    
    return None


def manage_key_render_categories(category_info:dict, category_list:list, sub_category_list:list, do_reload:bool=False)->tuple:
    id_current_cat:int = 0
    id_current_subcat:int = 0
    comment:str = None
    buffermode_on:bool = False
    key_buffer = []

    while True:
        render_cat_and_subcat(
            category_info=category_info,
            category_list=category_list,
            sub_category_list=sub_category_list, 
            id_current_cat=id_current_cat,
            id_current_subcat=id_current_subcat,
            key_buffer=key_buffer,
            buffermode_on=buffermode_on,
        )

        keypressed = getkey.getkey(blocking=True) 

        if keypressed == ":":
            buffermode_on = True
        
        if not buffermode_on:
            # Category navigation
            if keypressed == "h" or keypressed == getkey.keys.LEFT:
                id_current_cat -= 1
                if id_current_cat < 0:
                    id_current_cat = len(category_list) - 1
                id_current_subcat = 0
            elif keypressed == "l" or keypressed == getkey.keys.RIGHT:
                id_current_cat += 1
                if id_current_cat >= len(category_list):
                    id_current_cat = 0
                id_current_subcat = 0

            elif keypressed == "j" or keypressed == getkey.keys.DOWN:
                id_current_subcat += 1
            elif keypressed == "k" or keypressed == getkey.keys.UP:
                id_current_subcat -= 1
        
            # Category and sub-category selection
            elif keypressed == getkey.keys.ENTER:
                manage_and_render_query_and_selection(
                    category=category_info[category_list[id_current_cat]][sub_category_list[id_current_cat][id_current_subcat]], #category_list[id_current_cat],
                    identifier=sub_category_list[id_current_cat][id_current_subcat],
                    base_url=ArXurls.BASE_URL,
                    do_reload=do_reload,
                )

            elif keypressed == getkey.keys.ESC and not buffermode_on:
                clear()
                return 
            else:
                pass

        else:
            if keypressed == Cmd.EXIT:
                print()
                exit()
            elif keypressed == getkey.keys.ESC:
                key_buffer = []
                buffermode_on = False 
                print("\n")
            elif keypressed == getkey.keys.ENTER:
                print (key_buffer)
                buffermode_on = False
                key_buffer = []
            else:
                key_buffer.append(keypressed)
                    

def main(prefix:str=..., pdf_path:str=..., db_path:str=..., do_reload:bool=False):
    category_info:dict = {}
    with open(os.path.join(prefix, Paths.CATEGORIES_INFO), "r") as f:
        category_info = yaml.load(f, Loader=yaml.FullLoader)
    category_list = list(category_info.keys())
    sub_category_list = [list(category_info[cat].keys()) for cat in category_list] 
    manage_key_render_categories(category_info, category_list, sub_category_list, do_reload=do_reload)



if __name__ == "__main__":
    do_reload:bool = False
    for i in range(len(sys.argv)):
        if sys.argv[i] == "--prefix":
            prefix = sys.argv[i+1]
        elif sys.argv[i] == "--db":
            Paths.DB = sys.argv[i+1]
        elif sys.argv[i] == "--r":
            do_reload:bool = True
    
    main(prefix=prefix, pdf_path=Paths.PDF, db_path=Paths.DB, do_reload=do_reload)
