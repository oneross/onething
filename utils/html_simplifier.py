import re
import sys
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

    def get_data(self):
        # Join all text and then collapse multiple spaces and line breaks
        return re.sub(r'\s+', ' ', ''.join(self.text)).strip()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def extract_urls(html):
    urls = re.findall(r'href=["\'](.*?)["\']', html)
    urls += re.findall(r'src=["\'](.*?)["\']', html)
    # Filter out URLs that are likely to be JavaScript files
    urls = [url for url in urls if not url.endswith('.js')]
    return urls

def process_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    text = strip_tags(content)
    urls = extract_urls(content)

    print(text)
    print("\n---\n")
    print("### References\n")
    for url in urls:
        print(url)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
    else:
        process_file(sys.argv[1])