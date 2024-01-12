import getkey
from utils import (Cmd, clear)

def catch_kbd(MODE:str, key_instructions:dict=...)->dict:

    keypressed = getkey.getkey(blocking=True) 

    if MODE == "CAT":
        required_keys = [
            "id_current_cat", "id_current_subcat", 
            "kbd_ENTER", "kbd_ESC", "comment",
            "buffermode_on", "key_buffer",
            "category_list_len"
        ]

        assert [key in key_instructions.keys() for key in required_keys], f"""
        Call to (func) parse_cmd with {MODE} mode reqirs all {required_keys}"""

        id_current_cat:int = key_instructions["id_current_cat"]
        id_current_subcat:int = key_instructions["id_current_subcat"]
        kbd_ENTER = key_instructions["kbd_ENTER"]
        kbd_ESC = key_instructions["kbd_ESC"]
        comment:str = key_instructions["comment"]
        buffermode_on:bool = key_instructions["buffermode_on"]
        key_buffer:list = key_instructions["key_buffer"]
        category_list_len = key_instructions["category_list_len"]
        buffermode_on:str = False

        # if keypressed == ":":
        #     buffermode_on = True
        
        if not buffermode_on:
            # Category navigation
            if keypressed == "h" or keypressed == getkey.keys.LEFT:
                id_current_cat -= 1
                if id_current_cat < 0:
                    id_current_cat = category_list_len - 1
                id_current_subcat = 0
            elif keypressed == "l" or keypressed == getkey.keys.RIGHT:
                id_current_cat += 1
                if id_current_cat >= category_list_len:
                    id_current_cat = 0
                id_current_subcat = 0

            elif keypressed == "j" or keypressed == getkey.keys.DOWN:
                id_current_subcat += 1
            elif keypressed == "k" or keypressed == getkey.keys.UP:
                id_current_subcat -= 1
        
            # Category and sub-category selection
            elif keypressed == getkey.keys.ENTER:
                kbd_ENTER = True
                

            elif keypressed == getkey.keys.ESC and not buffermode_on:
                kbd_ESC = True

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
            
        key_instructions = {
            "id_current_cat" : id_current_cat,
            "id_current_subcat" : id_current_subcat,
            "comment" : comment,
            "buffermode_on" : buffermode_on,
            "key_buffer" : key_buffer,
            "kbd_ENTER" : kbd_ENTER,
            "kbd_ESC" : kbd_ESC,
        }

        return key_instructions

def handle_buffer(buffer:list=[])->None:
    assert type(buffer) == type([]), f"Buffer is expected to be a list, {type(buffer)} passed to (func) handle_buffer."
    input(buffer)
