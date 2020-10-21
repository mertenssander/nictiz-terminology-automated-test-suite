from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

def test_snomedbrowser_ptFriendly():
    req = Request("https://terminologie.nictiz.nl/terminology/snomed/viewConcept/74400008")
    response = urlopen(req).read()
    parsed_html = BeautifulSoup(response, features="html.parser")

    result = parsed_html.body.find('img', attrs={'src':'/terminology/resources/images/languageRefsets/15551000146102.png'}).parent.parent.parent
    result = result.find('div', attrs={'title':'Preferred term'}).text

    truth = "blindedarmontsteking"

    assert result == truth