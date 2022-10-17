import requests

def scraper():
    r = requests.get('https://www.simcoecountyschoolbus.ca/status.json')        # Make request to backend json file
    r = r.json()                                                                # convert request to json
    return r
    
def check(zone):
    response = scraper()
    if response[zone.title()]["status"] == "none":
        return f"🟩All busses running in the {zone.title()} zone"
    elif response[zone.title()]["status"] == "some":
        return f"🟨There are some cancellations in the {zone.title()} zone"
    elif response[zone.title()]["status"] == "all":
        return f"🛑All of the busses are cancelled in the {zone.title()} zone"