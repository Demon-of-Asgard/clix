import subprocess 
import os, sys, stat, platform, shutil

#=============================================================================#

_FAIL    = False
_SUCCESS = True 

src_files = [
    'db_manager.py', 
    'query_and_parse.py', 
    'LICENSE', 
    'renderer.py', 
    'cmd_state.py', 
    'install.sh', 
    'available_arxiv_categories.yaml', 
    'TODO.md', 
    'README.md', 
    'utils.py', 
    'arxiv_api_query.py', 
    'clix.sh', 
    'main.py', 
    'parse_kbd_cmd.py'
]

home_path   = os.path.expanduser("~")
src_path    = os.path.join("./", "src")
dst_path    = os.path.join(home_path, ".local", "clix", "src")
binary_src  = os.path.join("./", "clix")
db_path     = os.path.join(home_path, ".local", "clix", "db") 
binary_dst  = os.path.join("/", "usr", "local", "bin", "clix")
db_path_tmp = input(f"Enter absolute path to the destination where database to be stored.\n\
    Leave empty to store at {db_path} >"
) 
db_path     = db_path if db_path_tmp == "" else db_path_tmp
blob_path   = db_path

platform_type:str = "Linux"
shell:str         = "/bin/bash"

if platform.system() == "Darwin": 
    platform_type = "Mac"
    shell         = "/bin/zsh"

which_python = subprocess.check_output(["which", "python3"]).decode().strip()
print(f"{which_python=}")

#=============================================================================#

def create_dir(dir_path:str)->bool:
    
    if os.path.exists(dir_path):
        choice = input(f"{dir_path} already exist. Do you want to reinstall?[y/N] >").upper()
        if choice != "y".upper():
            print(f"You chose not to recreate {dir_path}")
            return _SUCCESS
    else:

        try:
            os.mkdir(dir_path)
        except Exception as E:
            print(E)
            return _FAIL
    
        
    return _SUCCESS

#=============================================================================#

def cp_file(src:str, dst:str)->bool:

    if not os.path.exists(src):
        print(f"[ ERROR ]Unable to find {src}.")
        return _FAIL
    
    if os.path.exists(dst):
        choice = input(f"{dst} already exist. Do you want to reinstall?[y/N] >").upper()
        if choice != "y".upper():
            print(f"You chose not to reinstall clix. Exiting setup.")
            exit(0)

    try:
        shutil.copy(src=src, dst=dst)
    except Exception as E:
        print(E)
        return _FAIL
        
    return _SUCCESS

#=============================================================================#

def cp_directory(src:str, dst:str)->bool:
    
    if not os.path.exists(src):
        print(f"[ ERROR ]Unable to find {src}.")
        return _FAIL
    
    if not os.path.exists(dst):
        try:
            os.makedirs(dst)
        except Exception as E:
            print(f"Exception raised while copying {src} to {dst}")
            print(E)
            return _FAIL
    else:
        choice = input(f"{dst} already exist. Do you want to reinstall?[y/N] >").upper()
        if choice != "y".upper():
            print(f"You chose not to reinstall clix. Exiting setup.")
            exit(0)
        
    try:
        for file in src_files:
            shutil.copy(src=os.path.join(src, file), dst=os.path.join(dst, file))
    except Exception as E:
        print(f"Exception raised while copytreeing {src}/* to {dst}/")
        print(E)
        return _FAIL

    return _SUCCESS

#=============================================================================#

def install_requirements(req_path:str)->bool:

    if not os.path.exists(req_path):
        print (f"{req_path} does not exists.")
        return _FAIL
    
    venv = sys.prefix.split("/")[-1]

    with open (req_path, "r") as f:
        packages = f.readlines()
    
    print(f"Going to install the following packages to your {venv=}")

    for pkg_i, pkg in enumerate(packages):
        print(f"\t({pkg_i+1}). {pkg.strip()}")

    status=""

    try:
        if input("[y/N]? > " ).upper() == "Y":
            status = subprocess.check_output(["pip3", "install", "-r", req_path]).decode()
            print(status)
    except Exception as e:
        print(f"[ ERROR ] Installation of the {[pkg.strip() for pkg in packages]} raised Exeption.")
        print("\tDetails:")
        print(f"\t\t{e}")
        return _FAIL
    
    return _SUCCESS

#=============================================================================#

def install()->bool:
    
    status:bool = cp_directory(src=src_path, dst=dst_path)
    if status == _FAIL: return _FAIL

    status = create_dir(dir_path=db_path)
    if not status:
        return _FAIL
    
    with open("clix", "w") as f:
        f.write("#!" + shell + "\n")
        command = f"{which_python} {os.path.join(dst_path, 'main.py')} --prefix {dst_path} --db {db_path} $@"
        f.write(f"{command}\n")

    try:
        command = f"chmod +x clix"
        os.system(command=command)
    except Exception as E:
        print(E)
        return _FAIL
    
    command = f"sudo mv clix {binary_dst}"
    try:
        print(f"Copying binary to {binary_dst}")
        os.system(command=command)
    except Exception as E:
        print(E)
        return _FAIL

    return _SUCCESS

#=============================================================================#


if __name__ == "__main__":
    if not install_requirements("requirements.txt"):
        print(f"[ ERROR ] Installation of the requirements failed. Exiting {__name__}.")
        exit(1)
    install()
    
