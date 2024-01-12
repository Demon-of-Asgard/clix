import os 
import sys
import yaml
import getkey
import pprint 
from arxiv_api_query import ArXapi
from utils import (Cmd, Os, Paths, ArXurls, clear, get_shell_text)
import renderer 
import parse_kbd_cmd as kbd


#------------------------------------------------------------------------------
def manage_key_render_categories(category_info:dict, category_list:list, sub_category_list:list, do_reload:bool=False)->tuple:
    id_current_cat:int = 0
    id_current_subcat:int = 0
    kbd_ENTER:bool = False
    kbd_ESC:bool = False
    comment:str = None
    buffermode_on:bool = False
    key_buffer:list = []

    required_keys = [
        "id_current_cat", "id_current_subcat",
        "comment", "buffermode_on",
        "key_buffer","kbd_ENTER", "kbd_ESC",
    ]
    while True:
        renderer.render_cat_and_subcat(
            category_info=category_info,
            category_list=category_list,
            sub_category_list=sub_category_list, 
            id_current_cat=id_current_cat,
            id_current_subcat=id_current_subcat,
            key_buffer=key_buffer,
            buffermode_on=buffermode_on,
        )
        current_cat_cmd_state = {
            "id_current_cat": id_current_cat,
            "id_current_subcat": id_current_subcat,
            "kbd_ENTER": kbd_ENTER,
            "kbd_ESC": kbd_ESC,
            "comment": comment,
            "buffermode_on": buffermode_on,
            "key_buffer": key_buffer,
            "category_list_len": len(category_list),
        }

        next_cat_cmd_state = kbd.catch_kbd(
            MODE="CAT",
            key_instructions = current_cat_cmd_state,
        )

        assert [key in next_cat_cmd_state.keys() for key in required_keys], f"""
        Return from (func) parse_cmd with CAT mode reqirs all {required_keys}"""
        
        id_current_cat = next_cat_cmd_state["id_current_cat"]
        id_current_subcat = next_cat_cmd_state["id_current_subcat"]
        kbd_ENTER = next_cat_cmd_state["kbd_ENTER"]
        kbd_ESC = next_cat_cmd_state["kbd_ESC"]
        comment = next_cat_cmd_state["comment"]
        buffermode_on = next_cat_cmd_state["buffermode_on"]
        key_buffer = next_cat_cmd_state["key_buffer"]

        if kbd_ESC:
            clear()
            return 
        elif kbd_ENTER:
            renderer.manage_and_render_query_and_selection(
                category=category_info[category_list[id_current_cat]][sub_category_list[id_current_cat][id_current_subcat]], 
                identifier=sub_category_list[id_current_cat][id_current_subcat],
                base_url=ArXurls.BASE_URL,
                do_reload=do_reload,
            )
            kbd_ENTER = False
                    

#------------------------------------------------------------------------------
def main(prefix:str=..., pdf_path:str=..., db_path:str=..., do_reload:bool=False):
    category_info:dict = {}
    with open(os.path.join(prefix, Paths.CATEGORIES_INFO), "r") as f:
        category_info = yaml.load(f, Loader=yaml.FullLoader)
    category_list = list(category_info.keys())
    sub_category_list = [list(category_info[cat].keys()) for cat in category_list] 
    manage_key_render_categories(category_info, category_list, sub_category_list, do_reload=do_reload)


#------------------------------------------------------------------------------
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

#------------------------------------------------------------------------------
