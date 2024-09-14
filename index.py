import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm

os.makedirs("archive", exist_ok=True)

pages = list(range(0, 1400, 200))

for i in tqdm(pages):
    r = requests.get(
        f"https://arxiv.org/search/?searchtype=all&query=Retrieval-augmented+generation&abstracts=show&size=200&order=-announced_date_first&start={i}"
    )

    soup = BeautifulSoup(r.content, "html.parser")

    s = soup.find_all("li", class_="arxiv-result")

    for j in tqdm(s):
        try:
            name = j.find("p", class_="title is-5 mathjax").text
            pdf_link = j.find("a", string="pdf")["href"]
            name = name.strip()
            name = name.replace(" ", "_").replace(":", "").replace("/", "_")

            res = requests.get(pdf_link)
            with open(os.path.join("archive", name + ".pdf"), "wb") as f:
                f.write(res.content)
        except Exception as e:
            print(f"Error occurred: {e}")
            continue
