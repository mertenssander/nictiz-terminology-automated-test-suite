from urllib.request import urlopen, Request
from urllib import parse
import json

def test_retrieve_singleConcept():
    """
    TEST
    """
    req = Request('https://snowstorm.test-nictiz.nl/MAIN/SNOMEDCT-NL/concepts/74400008')
    req.add_header('Accept-Language', 'nl')
    response = urlopen(req).read()
    data = json.loads(response)

    truth = {
            "conceptId" : "74400008",
            "active" : True,
            "definitionStatus" : "FULLY_DEFINED",
            "moduleId" : "900000000000207008",
            "effectiveTime" : "20020131",
            "fsn" : {
                "term" : "appendicitis (aandoening)",
                "lang" : "nl"
            },
            "pt" : {
                "term" : "appendicitis",
                "lang" : "nl"
            },
            "id" : "74400008"
        }

    assert data == truth