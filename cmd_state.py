class CmdState():
    def __init__(
            self, id_item:int=0, id_subitem:int=0, 
            kbd_ENTER:bool=False, kbd_ESC:bool=False,
            buffermode_on:bool=False, key_buffer:list=[],
            len_item:int=0, len_subitem:int=0,
            comment:str="",
        )->None:
        self.id_item:int = id_item
        self.id_subitem:int = id_subitem
        self.kbd_ENTER:bool = kbd_ENTER
        self.kbd_ESC:bool = kbd_ESC 
        self.buffermode_on:bool = buffermode_on
        self.key_buffer:list = key_buffer
        self.len_item:int = len_item
        self.len_subitem:int = len_subitem
        self.comment:str = comment
    