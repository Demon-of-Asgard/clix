import os 
import getkey
import datetime
import requests
import feedparser
import urllib.error
import urllib.request 
from utils import (Paths, Os, clear, get_shell_text)

class ArXapi():

    def __init__(self, category:str, identifier:str, base_url:str, reload:bool=False) -> None:

        self.category:str = category
        self.identifier:str = identifier
        self.base_url:str = base_url
        self.query:str = base_url
        self.reload:bool = reload
        
    def __str__(self):
        return self.identifier 
    
    def __repr__(self) -> str:
        return (f"cat: {self.category}" +"\n" + f"identifier: {self.identifier}" + "\n" + f"base_url: {self.base_url}")
    
    def construct_search_query(self, **kwargs) ->str:

        """ 
        From arXiv api description:
            If only search_query is given (id_list is blank or not given), 
            then the API will return results for each article that matches the search query.

            If only id_list is given (search_query is blank or not given), then the API 
            will return results for each article in id_list.

            If BOTH search_query and id_list are given, then the API will return each article 
            in id_list that matches search_query. This allows the API to act as a results filter.
        """

        self.query = f"{self.base_url}" + f"search_query="

        keys = kwargs.keys()

        # Adding category info to the query
        self.query += f"cat:{self.identifier}"
        
        # Adding sort method to the query
        if "sort_method" in keys:
            if kwargs['sort_method'] == "submitted_date":
                self.query += "&sortBy=submittedDate"
            elif kwargs['sort_method'] == "relevence":
                self.query += "&sortBy=relevence"
            elif kwargs['sort_method'] == "last_update_date":
                self.query += "&sortBy=lastUpdatedDate"
        else:
            self.query += "&sortBy=submittedDate"
        
        # Adding sort information to the query
        if "sort_order" in keys:
            if kwargs["sort_order"] == "descending":
                self.query += "&sortOrder=descending"
            else:
                self.query += "&sortOrder=ascending"
        else:
            self.query += "&sortOrder=ascending"

        # Adding query chunk information
        if "start_index" in keys:
            self.query +=  f"&start={kwargs['start_index']}"
        else:
            self.query +=  f"&start={0}"
        if "max_results" in keys:
            self.query += f"&max_results={kwargs['max_results']}"
        else:
            self.query += f"&max_results={0}"

        return self.query


    def make_query(self)->str:
        """Make query with urllib.request for self.query and handle the erroe using 
        urllib.errors.
        Accepted arguments: None,
        Request is made based on the value of self.query.
        """

        # Handle query and response to the request.
        
        try:
            with urllib.request.urlopen(self.query, timeout=120) as response:
                return response.status, response.read()
            
        except urllib.error.HTTPError as err: 
            print (f"HTTPError:\n\t{err.status}\n\t{err.reason}")
            return err.status, None
        except urllib.error.URLError as err:
            print (f"URLError:\n\tstatus={404}\n\t{err.reason}")
            return 404, None
        except TimeoutError as err:
            print("Request timeout")
            return None, None
    
    
    def parse_response(self, response:str)->list:
        '''Take response in xml format from query and parse using feed parser'''

        self.parsed_response = []
        feed = feedparser.parse(response)
        self.parsed_response = [entry for entry in feed.entries]
        return self.parsed_response


    def render_parsed_response(self):
        '''Render listed items from (func)parse_response and render as chunks of enumerated list.
        Also capture the key board inputs using geykey to navigate through list items.'''

        os.system("clear")
        comment = ""
        
        current_index = 0
        current_chunk_start = 0
        chunk_size = 20
        abs_index = -1

        while True:
            clear()
            print(get_shell_text(text= " ".join(self.category.split("_")).upper(), color="salmon", style="uline"))

            current_chunk = self.parsed_response[current_chunk_start:current_chunk_start + chunk_size]

            for index, entry in enumerate(current_chunk):
                title = (' '.join([element.strip() for element in entry['title'].split('\n')]) 
                            + " [" +entry['updated'].split("T")[0] + "]"
                )
                if index == current_index:
                    # Print title
                    print(f"[{index+current_chunk_start+1}] {get_shell_text(text = title, color='blue', style='bold')}")

                    if index == abs_index:
                        # Print authors name.
                        authlen = len(entry['authors']) if len(entry['authors']) <= 4 else 4
                        auth_list_end = f", +{len(entry['authors'])-4}" if len(entry['authors']) > 4 else ""
                        authors = ", ".join(auth['name'] for auth in entry['authors'][:authlen])
                        print(
                            get_shell_text(text=f"\t[{authors}{auth_list_end}]", color="green", style="italic")
                        )

                        #Print abstract
                        abstract_ = "\t\t" + "\n\t".join(entry['summary'].strip("<p>").strip("</p>").split("\n"))
                        abstract = get_shell_text(text=abstract_, color="grey", style="italic")
                        print(f"{abstract}", end = "\n")
                        url = "https://" + "".join(current_chunk[current_index]['link'].split("://")[1:])
                        print(f"\turl: {get_shell_text(text=url, color='blue', style='italic')}")

                else:
                    # title = ' '.join([element.strip() for element in entry['title'].split('\n')])
                    print(f"[{index+current_chunk_start+1}] {title}")
            
            if comment != None:
                print(comment)
            
            #get the key press
            key_pressed = getkey.getkey(blocking=True)
            comment = None 
            abs_index = -1
            
            if (key_pressed == getkey.keys.ESC):
                clear()
                return
            elif (key_pressed == "q"):
                clear()
                exit() 

            elif key_pressed == getkey.keys.DOWN or key_pressed == "j":
                # Increse current_index only if next index is in the chunk.
                # else, move to the next chunk, set current_index to 0
                if not (current_chunk_start + current_index >= (len(self.parsed_response) - 1)):
                    if ((current_index + 1) < chunk_size) and (current_chunk_start + current_index) < len(self.parsed_response): 
                        current_index += 1 
                    else: 
                        current_chunk_start += chunk_size
                        current_index = 0

            elif key_pressed == getkey.keys.UP or key_pressed == "k":
                # Decrease the current index by 1 only if (current_index-1) is in current chunk.
                # Else move tio the previous chunk if exist and set current_index to the last index of previous chunk.
                # Do nothing if there is no previous chunk to move to.
                if (current_chunk_start + current_index-1) >= current_chunk_start and (current_chunk_start + current_index-1) >= 0:
                    current_index -= 1 
                elif (current_chunk_start + current_index-1) < current_chunk_start and (current_chunk_start + current_index-1) >= 0:
                    current_chunk_start -= chunk_size
                    current_index = chunk_size-1
                elif (current_chunk_start + current_index-1) < 0:
                    pass 
            
            elif key_pressed == getkey.keys.RIGHT:
                # Set abs_index to current_index to show abstract
                abs_index = current_index
            elif key_pressed == getkey.keys.LEFT:
                # Close the abstract. This part is redundant.
                abs_index = -1

            elif key_pressed == getkey.keys.ENTER:
                # Enter to download and open the pdf
                stat = self.open_file(link=current_chunk[current_index]['link'])
            
            else:
                comment = get_shell_text(text="ERR: ", color="red", style="bold") + f"Unexpected Input <{key_pressed}>"
                continue
            
        return 
    

    def open_file(self, link:str)->None:

        pdf_folder = os.path.join(Paths.DB, Paths.PDF)
        if not os.path.exists(pdf_folder):
            try:
                os.makedirs(pdf_folder)
            except Exception as e:
                print(f"{get_shell_text(text='Exception', color='red', style='bold')}: {e.args}")

        pdf_path = os.path.join(pdf_folder, link.split("/")[-1] + ".pdf")

        if not os.path.exists(pdf_path):
            print(
                get_shell_text(text="downloading from arXiv", color="green") 
                + get_shell_text(text="...", color="green", style="blink")
            )

            url_of_id = "/pdf/".join(link.split("/abs/")) + ".pdf"
            response = requests.get(url_of_id)
            with open(pdf_path, "wb") as f:
                f.write(response.content)
        else:
            print(
                get_shell_text(text="loading from db", color="green") 
                + get_shell_text(text="...", color="green", style="blink")
            )

        os.system(f"{Os.OPEN} {pdf_path}")
        clear()
        return 


def main():
    obj = ArXapi(category="High Energy Astrophysics", identifier="astro#ph.HE", base_url="http://export.arxiv.org/api/query?")
   
    query = obj.construct_search_query(
        sort_method="submitted_date",
        sort_order="descenting",
        start_index=0,
        max_results=10,
    )
    print(f"{query=}")
    status, response = obj.make_query()
    parsed_response = obj.parse_response(response=response)
    print(f"{parsed_response}")


if __name__ == "__main__":
    main()

