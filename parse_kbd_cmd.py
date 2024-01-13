import getkey
from typing import Type

import cmd_state 
from utils import (Cmd, clear)


def catch_cat_navigation(current_nav_state:Type[cmd_state.CmdState]=...)->Type[cmd_state.CmdState]:

    nav_state = cmd_state.CmdState(
        id_item=current_nav_state.id_item, id_subitem=current_nav_state.id_subitem,
        kbd_ENTER=current_nav_state.kbd_ENTER, kbd_ESC=current_nav_state.kbd_ESC,
        buffermode_on=current_nav_state.buffermode_on, key_buffer=current_nav_state.key_buffer,
        len_item=current_nav_state.len_item, len_subitem=current_nav_state.len_subitem,
        comment=current_nav_state.comment,
    )

    keypressed = getkey.getkey(blocking=True) 
    # if keypressed == ":":
    #     buffermode_on = True
    
    if not nav_state.buffermode_on:
        # Category navigation
        if keypressed == "h" or keypressed == getkey.keys.LEFT:
            nav_state.id_item -= 1
            if nav_state.id_item < 0:
                nav_state.id_item = nav_state.len_item - 1
            nav_state.id_subitem = 0
        elif keypressed == "l" or keypressed == getkey.keys.RIGHT:
            nav_state.id_item += 1
            if nav_state.id_item >= nav_state.len_item:
                nav_state.id_item = 0
            nav_state.id_subitem = 0

        elif keypressed == "j" or keypressed == getkey.keys.DOWN:
            nav_state.id_subitem += 1
        elif keypressed == "k" or keypressed == getkey.keys.UP:
            nav_state.id_subitem -= 1
    
        # Category and sub-category selection
        elif keypressed == getkey.keys.ENTER:
            nav_state.kbd_ENTER = True
            

        elif keypressed == getkey.keys.ESC and not nav_state.buffermode_on:
            nav_state.kbd_ESC = True

        else:
            pass

    # else:
    #     if keypressed == Cmd.EXIT:
    #         print()
    #         exit()
    #     elif keypressed == getkey.keys.ESC:
    #         key_buffer = []
    #         buffermode_on = False 
    #         print("\n")
    #     elif keypressed == getkey.keys.ENTER:
    #         buffermode_on = False
    #         handle_buffer(buffer=key_buffer)
    #         key_buffer = []
    #     else:
    #         key_buffer.append(keypressed)
        
    return nav_state

def handle_buffer(buffer:list=[])->None:
    assert type(buffer) == type([]), f"Buffer is expected to be a list, {type(buffer)} passed to (func) handle_buffer."
    input(buffer)
