import os
import requests
import bs4
import argparse
from pathlib import Path

#TODO: Add different mirrors
#TODO: Add exception handling

url = "http://gen.lib.rus.ec/search.php?req={}&lg_topic=libgen&open=0&view=simple&res=25&phrase=1&column=def&sortmode=ASC&page={}" #LibGen URL

arg = argparse.ArgumentParser(description="A LibGen book downloader.")
arg.add_argument("book", help="enter a book name in quotes to search")
arg.add_argument("-v", "--version", action="version", version='Library Genesis Downloader 0.0.1')
#Lets the user specify a page to search in, might result in bugs
arg.add_argument("-p", "--page", help="enter a page to search in (default is 1)", type=int, default=1, action="store")
#If this is not specified the program will download the first available book
arg.add_argument("-i", "--interactive", help="interactive mode, displays available books in specified page", required=False, action="store_true")
args = arg.parse_args()

query = args.book.replace(" ", "+")
req = requests.get(url.format(query, args.page))

webpage = bs4.BeautifulSoup(req.text, features="lxml")
books = webpage.find("table", {"class": "c"})

book_list = []
book_links = []
book_names = []

tr = books.find_all('tr')
for i in tr:
    children = i.findChildren("td", {"width":"500"}, recursive=True)
    for child in children:
        book_list.append(str(child))
for book in book_list:
    parse = bs4.BeautifulSoup(book, features="lxml")
    book_links.append(parse.a['href'])
    book_names.append(parse.text)

def download_book(choice=1, interactive=False):
    chosen_link = book_links[int(choice) - 1]
    chosen_link = chosen_link[19:] 
    down_url = "http://93.174.95.29/_ads/" + chosen_link
    
    down = requests.get(down_url)
    down_page = "http://93.174.95.29" + bs4.BeautifulSoup(down.text, features="lxml").a['href']

    if interactive:
        name = input("Enter a filename(optional): ")
        if name != "":
            print("Downloading.")
            downloadfile = Path(name) #Manually naming the file
            filedata = requests.get(down_page)
            downloadfile.write_bytes(filedata.content)
            print("Download complete. Have a nice day!")
        else:
            print("Downloading.")
            os.system("wget " + down_page) #Downloads with wget to skip file naming
            print("Done.")
    else:
        os.system("wget " + down_page)

if args.interactive:
    count = 1
    for i in book_names:
        print(count, ":", i, "\n")
        count += 1
    choice = str(input("Press enter to exit interactive mode. Enter a number to download: "))
    if choice == "":
        print("Bye bye!")
    else:
        download_book(choice, True)
else:
    download_book(False)
        
