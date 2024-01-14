import getkey
from typing import Type

import cmd_state 
from utils import (Cmd, clear, get_shell_text)


def catch_cat_navigation(nav_state:Type[cmd_state.CmdState]=...)->Type[cmd_state.CmdState]:

    # nav_state = cmd_state.CmdState(
    #     id_item=current_nav_state.id_item, id_subitem=current_nav_state.id_subitem,
    #     kbd_ENTER=current_nav_state.kbd_ENTER, kbd_ESC=current_nav_state.kbd_ESC,
    #     buffermode_on=current_nav_state.buffermode_on, key_buffer=current_nav_state.key_buffer,
    #     len_item=current_nav_state.len_item, len_subitem=current_nav_state.len_subitem,
    #     comment=current_nav_state.comment,
    # )

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
            if nav_state.id_subitem < nav_state.len_subitem - 1:
                nav_state.id_subitem += 1
        elif keypressed == "k" or keypressed == getkey.keys.UP:
            if nav_state.id_subitem > 0:
                nav_state.id_subitem -= 1
    
        # Category and sub-category selection
        elif keypressed == getkey.keys.ENTER:
            nav_state.kbd_ENTER = True
            

        elif keypressed == getkey.keys.ESC:
            nav_state.kbd_ESC = True
        elif keypressed == "q":
            nav_state.do_quit = True

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


#------------------------------------------------------------------------------
def handle_buffer(buffer:list=[])->None:
    assert type(buffer) == type([]), f"Buffer is expected to be a list, {type(buffer)} passed to (func) handle_buffer."
    input(buffer)


#------------------------------------------------------------------------------
def parse_titles_pane_navigation(
        current_nav_state:Type[cmd_state.CmdState]=...
        )->Type[cmd_state.CmdState]:
    #get the key press
    key_pressed = getkey.getkey(blocking=True)
    
    if (key_pressed == getkey.keys.ESC):
        current_nav_state.kbd_ESC=True
    elif (key_pressed == "q"):
        current_nav_state.do_quit=True

    elif key_pressed == getkey.keys.DOWN or key_pressed == "j":
        # Increse current_nav_state.id_item only if next index is in the chunk.
        # else, move to the next chunk, set current_nav_state.id_item to 0
        if not (current_nav_state.id_item_start + current_nav_state.id_item >= (current_nav_state.len_item - 1)):
            if ((current_nav_state.id_item + 1) < current_nav_state.chunklen_item) and (current_nav_state.id_item_start + current_nav_state.id_item) < current_nav_state.len_item: 
                current_nav_state.id_item += 1 
            else: 
                current_nav_state.id_item_start += current_nav_state.chunklen_item
                current_nav_state.id_item = 0

    elif key_pressed == getkey.keys.UP or key_pressed == "k":
        # Decrease the current index by 1 only if (current_nav_state.id_item-1) is in current chunk.
        # Else move tio the previous chunk if exist and set current_nav_state.id_item to the last index of previous chunk.
        # Do nothing if there is no previous chunk to move to.
        if (current_nav_state.id_item_start + current_nav_state.id_item-1) >= current_nav_state.id_item_start and (current_nav_state.id_item_start + current_nav_state.id_item-1) >= 0:
            current_nav_state.id_item -= 1 
        elif (current_nav_state.id_item_start + current_nav_state.id_item-1) < current_nav_state.id_item_start and (current_nav_state.id_item_start + current_nav_state.id_item-1) >= 0:
            current_nav_state.id_item_start -= current_nav_state.chunklen_item
            current_nav_state.id_item = current_nav_state.chunklen_item-1
        elif (current_nav_state.id_item_start + current_nav_state.id_item-1) < 0:
            pass 
    
    elif key_pressed == getkey.keys.RIGHT:
        # Set abs_index to current_nav_state.id_item to show abstract
        current_nav_state.id_subitem = current_nav_state.id_item
    elif key_pressed == getkey.keys.LEFT:
        # Close the abstract. This part is redundant.
        current_nav_state.id_subitem = -1

    elif key_pressed == getkey.keys.ENTER:
        # Enter to download and open the pdf
        current_nav_state.kbd_ENTER=True
    else:
        current_nav_state.comment = get_shell_text(text="ERR: ", color="red", style="bold") + f"Unexpected Input <{key_pressed}>"

    return current_nav_state
