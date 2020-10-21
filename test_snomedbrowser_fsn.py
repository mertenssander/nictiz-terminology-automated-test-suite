from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

def test_snomedbrowser_fsn():
    req = Request("https://terminologie.nictiz.nl/terminology/snomed/viewConcept/74400008")
    response = urlopen(req).read()
    parsed_html = BeautifulSoup(response, features="html.parser")

    fsn = str(parsed_html.body.find('span', attrs={'style':'font-size:110%;font-weight:bold;'}).text)
    truth = "appendicitis (aandoening)"

    assert fsn == truth