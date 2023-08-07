import requests
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()


# soup = BeautifulSoup(html_doc, 'html.parser')


def save(fileName, data):
    with open(fileName, "w", encoding='utf-8') as f:
        f.write(data)


def fetch(url):
    proxies = {
        "http": "",  # Get your proxies from any services like Live Proxies.
        "https": "",
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/39.0.2171.95 Safari/537.36'}
    # headers = {
    #     'User-Agent': ua.ie}
    r = requests.get(url, headers=headers, proxies=proxies)
    return r.text


def extract_Links(html):
    soup = BeautifulSoup(html, 'html.parser')
    required_links = set()
    for link in soup.find_all("a", href=True):
        if "/dp/" in link['href']:
            required_links.add(link)

    return required_links


def extractor(html):
    data = {}
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find("span", {"id": "productTitle"}).get_text()
    data["title"] = title

    features = soup.find("div", {"id": "feature-bullets"})
    data["features"] = []
    for li in features.find("li"):
        data["features"].append(li.get_text())

    prices = soup.find("span", {"class": "a-price-whole"}).get_text()
    data["price"] = prices

    reviewsDiv = soup.find("div", {'class': "cm-cr-dp-reviews-list"})
    divs = reviewsDiv.findChildren("div",recursive=False)
    data["reviews"] = []
    for div in divs:
        data["reviews"].append(div.get_text())

    return data


if __name__ == "__main__":
    print('Starting to collect data')
    query = "monitor"
    url = f"https://www.amazon.com/s?k={query}"
    text = fetch(url)
    save('index.html', text)
    links = extract_Links(text)
    print(links)
    #  Transferring data to CSV
    finalData = []

    try:
        for link in links:
            print(link)
            content = fetch(f"https://amazon.in{link}")
            # save("product.html", content)
            a = extractor(content)
            print(a)
            finalData.append(a)
    except Exception as e:
        print(e)

    df = pd.DataFrame(finalData)
    df.to_csv("dataExtract.csv")
