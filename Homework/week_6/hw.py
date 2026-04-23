# task 1
import requests

response = requests.get("https://random-word-api.herokuapp.com/word")
word = response.json()[0]

if len(word) <= 2:
    hangman = word
else:
    hangman = word[0] + '-' * (len(word) - 2) + word[-1]

print(f"Word has {len(word)} letters: {hangman}")

# task 2
import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
headings = soup.find_all("h2")

print(f"H2 headings found on {url}:\n")
for i, h in enumerate(headings, 1):
    print(f"{i}. {h.get_text(strip=True)}")


