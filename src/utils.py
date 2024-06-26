import os
import platform


class Cmd:
    NEXT = "n"
    PREVIOUS = "p"
    ABSTRACT = "a"
    OPEN = "o"
    EXIT = "q"

class ArXurls:
    BASE_URL = "http://export.arxiv.org/api/query?"

    
class Os:
    TYPE = platform.system()
    OPEN = 'open' if TYPE == 'Darwin' else 'xdg-open'


class Paths:
    PDF = "pdf"
    DB  = "db"
    DB_NAME = "arxive_db"
    CATEGORIES_INFO = "available_arxiv_categories.yaml"

class Fields:
    fields = [
        ("astro-ph.GA" , 1),
        ("astro-ph.CO" , 2), 
        ("astro-ph.EP" , 3), 
        ("astro-ph.HE" , 4), 
        ("astro-ph.IM" , 5), 
        ("astro-ph.SR" , 6), 
        ("cond-mat.dis-nn" , 7), 
        ("cond-mat.mtrl-sci" , 8), 
        ("cond-mat.mes-hall" , 9),
        ("cond-mat.other" , 10), 
        ("cond-mat.quant-gas",  11),
        ("cond-mat.soft" , 12),
        ("cond-mat.stat-mech", 13),
        ("cond-mat.str-el" , 14),
        ("cond-mat.supr-con" , 15),
        ("gr-qc", 16),
        ("hep-ph", 17),
        ("hep-lat" , 18), 
        ("hep-ex" , 19), 
        ("hep-th" , 20),
    ]

    
def clear()-> None:
    os.system("clear")
    return None



def get_shell_text(text: str="",  color: str = "default", style: str = "default") -> str:
    """Create colorful custom shell texts. """
    if Os.TYPE != 'Darwin':
        shell_styles = {"default": 0, "bold": 1, "faded": 2,
                            "italic": 3, "uline": 4, "blink": 5, "bg": 7}

        shell_colors = {"default": 0, "blue": 30, "red": 31, "green": 32,
                        "yellow": 33, "purple": 35, "cyan": 36,  "grey": 37}
    else:
        shell_styles = {"default": 0, "bold": 1, "faded": 2,
                            "italic": 3, "uline": 4, "blink": 5, "bg": 7}

        shell_colors = {"default": 0, "blue": 34, "red": 31, "green": 32,
                        "yellow": 33, "purple": 35, "cyan": 36,  "grey": 37}
        
    return f'\033[{shell_styles[style]};{shell_colors[color]}m{text}\033[0m'


# def move_cursor_by(up:int=0, right:int=0):
#     print("\033[%d;%dH" %(right, up))

#     print(f"\r{'['}{'='*(l)}{'-'*(100-l)}{l}{'%]'}", end="")

