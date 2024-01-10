import os 
import sys
import yaml
import getkey
import pprint 
import datetime
from arxiv_api_query import ArXapi
from utils import (Cmd, Os, Paths, ArXurls, clear, get_shell_text)

def manage_and_render_query_and_selection(category:str=..., identifier:str=..., base_url:str=...):

    start_index=0
    max_results=100

    query_obj = ArXapi(
        category=category,
        identifier=identifier,
        base_url=base_url,
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
    if not os.path.exists(qury_save_file):
        query = query_obj.construct_search_query(
            sort_method="submitted_date",
            sort_order="descenting",
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


def render_categories(category_info:dict, category_list:list, sub_category_list:list)->tuple:
    id_current_cat:int = 0
    id_current_subcat:int = 0
    comment:str = None
    key_buffer = []
    while True:
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
                        print(f"\t{get_shell_text(text=f'[{j}] {category_info[cat][sub_cat]}', color='blue')}")
                    else:
                        print(f"\t[{j}] {category_info[cat][sub_cat]}")
            else:
                print(f"[{i}] {cat}")
           
        # Capturing key press     
        keypressed = getkey.getkey(blocking=True) 

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
                base_url=ArXurls.BASE_URL
            )
        
        elif keypressed == Cmd.EXIT:
            os.system("clear")
            exit()

        elif keypressed == getkey.keys.ESC:
            clear()
            return 
        else:
            print(keypressed, end="")
            input()



def main(prefix:str=..., pdf_path:str=..., db_path:str=...):
    category_info:dict = {}
    with open(os.path.join(prefix, Paths.CATEGORIES_INFO), "r") as f:
        category_info = yaml.load(f, Loader=yaml.FullLoader)
    category_list = list(category_info.keys())
    sub_category_list = [list(category_info[cat].keys()) for cat in category_list] 
    render_categories(category_info, category_list, sub_category_list)



if __name__ == "__main__":
    prefix="./"
    pdfat = "./"
    for i in range(len(sys.argv)):
        if sys.argv[i] == "--prefix":
            prefix = sys.argv[i+1]
        elif sys.argv[i] == "--pdf":
            Paths.PDF = sys.argv[i+1]
        elif sys.argv[i] == "--db":
            Paths.DB = sys.argv[i+1]
        else:
            pass
    
    main(prefix=prefix, pdf_path=Paths.PDF, db_path=Paths.DB)
