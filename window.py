import tkinter as tk
import requests
from bs4 import BeautifulSoup
import json

def scrapeURL():
    url_entry = url.get()

    num_selectors = int(nr_selectors_var.get())

    selectors = [selector_entries[i].get() for i in range(num_selectors)]

    response = requests.get(url_entry)
    if response.status_code == 200:
        html_content = response.text

        scraped_data = {}

        soup = BeautifulSoup(html_content, 'html.parser')

        text_data = []
        img_data = []

        for selector in selectors:
            elements = soup.select(selector)
            if "img" in selector:
                img_data.extend([element['src'] for element in elements])
            else:
                text_data.extend([element.get_text().strip() for element in elements])

        for i, text in enumerate(text_data):
            scraped_data[f'text{i+1}'] = text

        for i, img_src in enumerate(img_data):
            scraped_data[f'image{i+1}'] = img_src

        try:
            with open('scraped_data.json', 'r') as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = []

        existing_data.append(scraped_data)

        with open('scraped_data.json', 'w') as f:
            json.dump(existing_data, f, indent=4)

        print("Scraping completed. Data appended to 'scraped_data.json'")
    else:
        print("Failed to fetch webpage")


window = tk.Tk()
window.title('Telegrafi WS')
window.minsize(800, 600)

url_label = tk.Label(window, text="URL:")
url = tk.Entry(window)
url_label.pack()
url.pack()

nr_selectors_label = tk.Label(window, text="# Selectors:")
nr_selectors_var = tk.StringVar()
nr_selectors = tk.Entry(window, textvariable=nr_selectors_var)
nr_selectors_label.pack()
nr_selectors.pack()

def on_nr_selectors_change(*args):
    ns = int(nr_selectors_var.get())
    for i in range(1, ns+1):
        efl = tk.Label(window, text=f"Selector #{i}:")
        efl.pack()
        ef = tk.Entry(window)
        ef.pack()
        selector_entries.append(ef)

    nl = tk.Label(window, text=f"")
    nl.pack()
    sbtn = tk.Button(window, text="Scrape", command=scrapeURL)
    sbtn.pack()

nr_selectors_var.trace("w", on_nr_selectors_change)

selector_entries = []

window.mainloop()
