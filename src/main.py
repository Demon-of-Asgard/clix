import os 
import sys
import yaml
import getkey

import renderer 
import cmd_state
import parse_kbd_cmd as kbd
import query_and_parse as qap 
from arxiv_api_query import ArXapi
from utils import (
    Cmd, Os, Paths, ArXurls, clear, get_shell_text
)
import db_manager as db_manager


#------------------------------------------------------------------------------
def manage_key_render_categories(
        category_info:dict, category_list:list, 
        sub_category_list:list, do_reload:bool=False)->tuple:
    
    nav_state = cmd_state.CmdState(
        id_item=0, id_subitem=0, 
        kbd_ENTER=False, kbd_ESC=False, 
        buffermode_on=False, key_buffer=[],
        len_item=len(category_list), len_subitem=len(sub_category_list[0]),
        comment="",
    )
    
    while True:
        renderer.render_cat_and_subcat(
            category_info=category_info,
            category_list=category_list,
            sub_category_list=sub_category_list[nav_state.id_item], 
            id_current_cat=nav_state.id_item,
            id_current_subcat=nav_state.id_subitem,
            key_buffer=nav_state.key_buffer,
            buffermode_on=nav_state.buffermode_on,
        )

        nav_state = kbd.catch_cat_navigation(
            nav_state=nav_state,
        )
        nav_state.len_subitem = len(sub_category_list[nav_state.id_item])
        if nav_state.do_quit:
            clear()
            exit()
        elif nav_state.kbd_ESC:
            clear()
            return 
        elif nav_state.kbd_ENTER:
            nav_state.kbd_ENTER = False
            category = category_info[category_list[nav_state.id_item]][sub_category_list[nav_state.id_item][nav_state.id_subitem]]
            identifier=sub_category_list[nav_state.id_item][nav_state.id_subitem]
            parsed_response = qap.make_query_and_parse(
                category=category, 
                identifier=identifier,
                base_url=ArXurls.BASE_URL,
                do_reload=do_reload,
            )
            
            db_manager.add_to_db(parsed_data=parsed_response, category=category, identifier=identifier)
            
            ############## PARSED RESPONSE ##############
            navstate_parsed_response = cmd_state.CmdState(
                id_item=0, id_subitem=-1,
                id_item_start=0, id_subitem_start=-1,
                kbd_ENTER=False, kbd_ESC=False,
                buffermode_on=False, key_buffer=[], 
                chunklen_item=25, chunklen_subitem=-1, 
                len_item=len(parsed_response), len_subitem=-1,
                comment="",
            )
            while True:
                renderer.render_parsed_response(
                    parsed_response= parsed_response, 
                    display_title=category_info[category_list[nav_state.id_item]][sub_category_list[nav_state.id_item][nav_state.id_subitem]],
                    identifier=sub_category_list[nav_state.id_item][nav_state.id_subitem],
                    navigation_state=navstate_parsed_response,
                )

                navstate_parsed_response = kbd.parse_titles_pane_navigation(
                    current_nav_state=navstate_parsed_response
                )
                if navstate_parsed_response.do_quit == True:
                    clear()
                    exit()
                elif navstate_parsed_response.kbd_ESC == True:
                    break
                elif navstate_parsed_response.kbd_ENTER == True:
                    stat = ArXapi.open_file(
                        link=parsed_response[navstate_parsed_response.id_item_start+navstate_parsed_response.id_item]['link']
                    )
                    navstate_parsed_response.kbd_ENTER = False
                else:
                    continue
                    

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
