import requests

def scraper():
    r = requests.get('https://www.simcoecountyschoolbus.ca/status.json')        # Make request to backend json file
    r = r.json()                                                                # convert request to json
    return r
    
def check(zone):
    response = scraper()
    return response[zone.title()]["status"]
