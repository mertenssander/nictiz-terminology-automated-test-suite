from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

def test_snomedbrowser_version():
    req = Request("http://terminologie.nictiz.nl/art-decor/snomed-ct")
    response = urlopen(req).read()
    parsed_html = BeautifulSoup(response, features="html.parser")

    result = parsed_html.body.find('span', attrs={'id':'xf-337≡≡c'}).text

    truth = "SNOMED Clinical Terms version: 20200731 [R] (July 2020 Release)"

    assert result == truth