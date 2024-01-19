import os
import sys
import getkey
import datetime
from typing import Type
from arxiv_api_query import ArXapi
import cmd_state
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
        if i == id_current_cat:
            print(f"[{i}] " + get_shell_text(
                text=cat, color='grey', style='bg'))
            
            for j, sub_cat in enumerate(sub_category_list):
                if id_current_subcat >= len(sub_category_list):
                    id_current_subcat = 0
                if id_current_subcat < 0:
                    id_current_subcat = len(sub_category_list) -1 
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
def render_parsed_response(
        parsed_response:list=[], display_title:str="", identifier:str="",
        navigation_state:Type[cmd_state.CmdState]=None)->None:
    '''Render listed items from (func)parse_response and render as chunks of enumerated list.
    Also capture the key board inputs using geykey to navigate through list items.'''

    clear()
    print(get_shell_text(text= " ".join(display_title.split("_")).upper(), color="red", style="uline"))
    checked_cross_ref:bool = False
    current_chunk = parsed_response[navigation_state.id_item_start:navigation_state.id_item_start + navigation_state.chunklen_item]

    for index, entry in enumerate(current_chunk):
        if entry['arxiv_primary_category']['term'] != identifier and checked_cross_ref != True:
            print(get_shell_text(text= "[" + "cross references".upper() + "]", color="red", style="uline"))
            checked_cross_ref = True

        title = (' '.join([element.strip() for element in entry['title'].split('\n')]) 
                    + " [" +entry['updated'].split("T")[0] + "]"
        )
        if index == navigation_state.id_item:
            # Print title
            print(f"[{index+navigation_state.id_item_start+1}] {get_shell_text(text = title, color='blue', style='bold')}")

            if index == navigation_state.id_subitem:
                # Print authors name.
                authlen = len(entry['authors']) if len(entry['authors']) <= 4 else 4
                auth_list_end = f", +{len(entry['authors'])-4}" if len(entry['authors']) > 4 else ""
                authors = ", ".join(auth['name'] for auth in entry['authors'][:authlen])
                primary_cat = get_shell_text(text=f"[{entry['arxiv_primary_category']['term']}]", color='red', style="bold")
                auth_list = get_shell_text(text=f"[{authors}{auth_list_end}]", color="green", style="italic")
                url = "https://" + "".join(current_chunk[navigation_state.id_item]['link'].split("://")[1:])
                print(f"\t{auth_list} {primary_cat}")
                print(f"\turl: {get_shell_text(text=url, color='blue', style='italic')}")

                #Print abstract
                abstract_ = "\t\t" + "\n\t".join(entry['summary'].strip("<p>").strip("</p>").split("\n"))
                abstract = get_shell_text(text=abstract_, color="grey", style="italic")
                print(f"{abstract}", end = "\n")

        else:
            # title = ' '.join([element.strip() for element in entry['title'].split('\n')])
            print(f"[{index+navigation_state.id_item_start+1}] {title}")
        
        if navigation_state.comment != "":
            print(navigation_state.comment)
        
    return None 
