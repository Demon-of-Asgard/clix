class CmdState():
    def __init__(
            self, id_item:int=0, id_subitem:int=0, 
            id_item_start=0, id_subitem_start=0,
            kbd_ENTER:bool=False, kbd_ESC:bool=False,
            buffermode_on:bool=False, key_buffer:list=[],
            chunklen_item:int=0, chunklen_subitem=-1,
            len_item:int=0, len_subitem:int=0,
            do_quit:bool=False,comment:str="",
        )->None:

        self.id_item:int = id_item
        self.id_subitem:int = id_subitem
        self.id_item_start=id_item_start
        self.id_subitem_start=id_subitem_start
        self.kbd_ENTER:bool = kbd_ENTER
        self.kbd_ESC:bool = kbd_ESC 
        self.buffermode_on:bool = buffermode_on
        self.key_buffer:list = key_buffer
        self.chunklen_item:int=chunklen_item
        self.chunklen_subitem:int=chunklen_subitem
        self.len_item:int = len_item
        self.len_subitem:int = len_subitem
        self.do_quit:bool=do_quit
        self.comment:str = comment
    