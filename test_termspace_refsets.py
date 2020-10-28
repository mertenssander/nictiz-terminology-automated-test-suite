import os
from urllib.request import urlopen, Request
from urllib import parse
import json
import pytest

def test_retrieve_token():
    payload = {
        'username' : os.getenv('termspace_bot_user'),
        'password' : os.getenv('termspace_bot_pass'),
        }
    data = parse.urlencode(payload).encode('ascii')
    req = Request('https://nl-prod-main.termspace.com/api/users/login', data)
    with urlopen(req) as response:
        result = json.loads(response.read())

    termspace_token = result.get('token',False)
    assert termspace_token != False
    return termspace_token

def test_termspace_devPath_refsetCount_onlyActive():
    token = test_retrieve_token()

    if not token:
        pytest.fail("Geen token ontvangen")
    else:
        path = '112'

        # Get refset member counts termspace
        req = Request('https://nl-prod-main.termspace.com/api/server/releases?access_token='+token)
        termspace = json.loads(urlopen(req).read())
        version = termspace[-1]
        print(f"Testen met versie {version['collectionName']} / path {path}")
        refsets = version.get('refsets')

        # Lijst met refsets die niet door NL beheerd worden of niet in termspace staan
        uitzonderingen = [
            '900000000000490003',   # referentieset met attribuutwaarden voor reden voor deactivatie van beschrijving (metadata)
            '15551000146102',       # ? geen FSN en bevat niets
            '900000000000497000',   # CTV3 simple map reference set (foundation metadata concept)
            '762103008',            # OWL ontology reference set (foundation metadata concept)
            '733073007',            # OWL axiom reference set (foundation metadata concept)
            '900000000000498005',   # SNOMED RT identifier simple map (foundation metadata concept)
            '467614008',            # GMDN simple map reference set (foundation metadata concept)
            '447562003',            # ICD-10 complex map reference set (foundation metadata concept)
            '900000000000509007',   # Amerikaans-Engelse taalreferentieset (metadata)
            '31000146106',          # Nederlandse taalreferentieset (foundation metadata concept)
            '900000000000531004',   # REFERS TO concept association reference set (foundation metadata concept)
            '900000000000489007',   # Concept inactivation indicator attribute value reference set (foundation metadata concept)
            '900000000000508004',   # Brits-Engelse taalreferentieset (foundation metadata concept)

            '723562003',            # MRCM attribute range international reference set (foundation metadata concep
            '900000000000523009',   # historical poss eq
            '723561005',            # MRCM attribute domain international reference set (foundation metadata concept)
            '90000000000045600',    # MRCM attribute domain international reference set (foundation metadata concept)
            '900000000000526001',   # Replaced by
            '900000000000527005',   # Same as
            '900000000000456007',   # Reference set descriptor reference set (foundation metadata concept)
            '900000000000530003',   # Alternative
            '900000000000534007',   # Module dependency refset
            '900000000000528000',   # Was a
            '723563008',            # MRCM module scope reference set (foundation metadata concept)
            '446608001',            # ICD-O simple map reference set (foundation metadata concept)
        ]

        failed = False
        fails = 0

        req = Request('https://snowstorm.test-nictiz.nl/browser/MAIN%2FSNOMEDCT-NL/members?active=true&offset=0&limit=1')
        snowstorm = json.loads(urlopen(req).read())

        for refset in snowstorm.get('memberCountsByReferenceSet'):
            ## refset = refset conceptid
            try:
                if (refset not in uitzonderingen):
                    url = 'https://nl-prod-main.termspace.com/api/snomed/nl-edition/v'+version['collectionName']+'/concepts/'+refset+'/members?limit=1&pathId='+path+'&paginate=1&access_token='+token
                    req = Request(url)
                    result = json.loads(urlopen(req).read())
                    if (result['details']['total'] != snowstorm.get('memberCountsByReferenceSet').get(refset)):
                        print(f"[refset {refset}: termspace {result['details']['total']} / snowstorm {snowstorm.get('memberCountsByReferenceSet').get(refset)}]")
                        failed = True
                        fails += 1
            except KeyError:
                print(f"Kon {refset} niet testen - niet aanwezig in Termspace")
                failed = True
                fails += 1
            except Exception as e:
                print(f"Onbekende fout: {str(e)}")
                print(f"URL = {url} / refset = {refset}")
                failed = True
                fails +=1
        if failed:
            pytest.fail(f"Version [{version['collectionName']}] - [{fails} fouten in {len(snowstorm.get('memberCountsByReferenceSet'))} refsets]")