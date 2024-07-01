import urllib.request
import json
import secret

def getMediaID(title: str) -> int:
    """
    Runs the Autocomplete API to get the media ID
    """
    link = f"https://api.watchmode.com/v1/autocomplete-search/?apiKey={secret.APIKEY}&search_value={title}&search_type=1"
    request = urllib.request.Request(link, headers={"User-Agent": "Mozilla/5.0"})
    response = urllib.request.urlopen(request)
    results = json.loads(response.read())

    try:
        return results["results"][0]["id"]
    
    except IndexError:
        return -1

def getStreamingSources(mediaID: int) -> list:
    """
    Gets a list of streaming services that have mediaID
    """
    link = f"https://api.watchmode.com/v1/title/{mediaID}/details/?apiKey={secret.APIKEY}&append_to_response=sources"
    request = urllib.request.Request(link, headers={"User-Agent": "Mozilla/5.0"})
    response = urllib.request.urlopen(request)
    results = json.loads(response.read())

    sources = set()

    for entry in results["sources"]:
        if entry["region"] == "US" and entry["type"] == "sub":
            sources.add(entry["name"])

    return sorted(list(sources))

def prepareTitleNames(name: str) -> str:
    """
    Prepares the name for a URL
    """
    return name.replace(" ", "%20")



if __name__ == "__main__":
    title = "Iron Man"
    mediaID = getMediaID(prepareTitleNames(title))

    if mediaID != -1:
        sources = getStreamingSources(mediaID)
        print(sources)
