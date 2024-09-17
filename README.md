<div align="center">
	<img src="imgs/clix.png">
</div>

Sometimes I find browsers very distracting. So I wrote some simple scipts in `python` and named it `clix` (CLI-arXiv). `clix` uses arXiv API to perform the the queries and `sqlite3` to store metadata. `clix` allow one to bowse arxiv entried on terminal and read articles and open pdf file on the default pdf reader. Feel free to use, modify and distribute according to the MIT lisence.

## Install 
1. Clone the repository 
```shell
git clone git@github.com:Demon-of-Asgard/clix.git
```
2. Change directory to the `clix` folder 
```shell
cd clix
```
3. Run setup (you may need to provide user password if and when asked)
```shell
python setup.py
```

This will copy all the necessary source files and create necessary folders. 

Run `clix` on the terminal to bowse arxiv. 
Run `clix --reload` or `clix -r` to reload

## Navigation
1. Quit: Press `q`
2. Previous page: `esc`
3. Category page:
    - `Left` and `Right` arrow to navigate main cetegories. You could also use `h` and `l` keys (as in `vim`) for the same purpose.
    - `Up` and `Down` arrow to navigate through sub-cetegories. You could also use `i` and `j` keys.
    - `Enter` to open the current sub-category .
4. Sub-category page:
    - `Right` (`Left`) arrows to reveal(un-reveal) the abstract.
    - `Enter` to open pdf of the current selection in the default pdf reader.