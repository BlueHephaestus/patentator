"""


"""
import re
from serpapi import GoogleSearch
# CoinGecko
from utils.ai_utils import *
import requests
import threading

TEST_PATENT_ID = "US20230027590A1"
def get_with_default(data, keys, default=None):
    """
    Because no matter how many times I code this and no matter how many cases I account for,
    I always have to get data from dictionaries or from responses to API requests, and let's just, you know what,
    i'm gonna use this docstring to talk about my anger with this.

    Let's say you want to get the "items" dictionary in a Birdeye api call. Well you would make an API request,
    then get, ideally (funny how often we end up saying that), {"data": "items": [a, b, c d] } as the response,
    then you'd reference data, and reference items from that.

    Except, any of the following can happen and WILL happen, at EACH point we get a value from the dict:
    * The request gives an error
    * The request returns None
    * The reqeust returns {}
    * The request returns a dict with other keys in it but not 'data'
    * The request returns a dict with data in it but with None as the value
    * The request returns a dict with data in it but with an empty dict as the value
    * This repeats for every layer of referencing.

    SO.

    This function will recursively try to get these values so that if it fails at any point it will return the default
        and NOT ERROR. If it reaches an error at any point, it will also return the default.

    :param data: Any value to reference with 'key'. May be None, may be an int, may be a dict.
        Should be a dict, or a list, but who knows nowadays.
    :param keys: List of 'keys' to reference 'data' with. If ['data','items'], will try to do data['data']['items'].
        These will be popped from the front as we recurse. COULD BE INTEGERS OR STRINGS
    :param default: Default value to return if anything goes wrong.
    :return:
    """
    try:
        if data is None:
            return default
        if not isinstance(data, dict) and not isinstance(data, list):
            return default
        if data == {} or data == []:
            return default
        if len(keys) == 0:
            return default
        key = keys.pop(0)
        if isinstance(key, int) and len(data) <= key: # list case
            return default
        if isinstance(key, str) and key not in data: # dict case
            return default

        if data[key] is None:
            return default

        if data[key] == {} or data[key] == []:
            return default

        # FINALLY, BASE CASE RECURSIVE CASE
        if len(keys) == 0:
            # Last key, return the value
            return data[key]
        else:
            # Not last key, return the recursive call
            return get_with_default(data[key], keys, default)

    except:
        return default

# shorthand
def gwd(data, keys, default=None):
    return get_with_default(data, keys, default)

LINE_NUMBER_REGEX = re.compile(r'\s*\d+(?:\.\d+)*\.\s*', flags=re.UNICODE)
def remove_numbering(line):
    return LINE_NUMBER_REGEX.sub(' ', line).strip()

LINK_REGEX = re.compile(r'\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b', flags=re.UNICODE)
def get_links(line):
    """
    Generic get links from a line of text, will return a list of links or empty list if none.

    :param line:
    :return:
    """
    return LINK_REGEX.findall(line)


OUTSIDE_REGEX = re.compile(r'[\[({].*?[\])}]', flags=re.UNICODE)
def outside(line):
    """
    Given line, return the substr not inside any delimiters
    e.g. asdf (somelink.com) -> somelink.com
    """
    return OUTSIDE_REGEX.sub('', line)

CLEAN_REGEX = re.compile(r'[^a-zA-Z0-9_\-\.]+', flags=re.UNICODE)
def clean(line):
    return CLEAN_REGEX.sub(' ', line).strip()

# print(line, "|", re.sub(, ' ', line, flags=re.UNICODE))
def get_name(line):
    # get the name from the first line of the entry
    line = clean(remove_numbering(outside(line)))
    if line.endswith("-"):
        line = line[:-1].strip()
    return line

def get_link(entry):
    links = get_links(entry)
    if len(links) > 0:
        return links[0]
    return ""

def get_classification(line):
    classification = clean(remove_numbering(outside(line)))
    if classification.lower() == "yes":
        return 2
    elif classification.lower() == "no":
        return 0
    return 1 # unknown / unsure

class API:
    def __init__(self, test_keys=True):
        self.keys = []
        self.key = ''
        self.base_url = 'URL with endpoint in {}'
        self.base_headers = {}
        if test_keys:
            pass

    def next_api_key(self):
        self.key = self.keys[(self.keys.index(self.key) + 1) % len(self.keys)]
        self.base_headers['X-API-KEY'] = self.key
        return self.key

    def request(self, *args, **kwargs):
        pass

class SerpApi(API):
    def __init__(self, test_keys=True):
        self.keys = [
            "6328b60d23198d8e3ef25bad85cc2760b9b3fa4de8a83bdb0bfc0fc124714dcd",
            "3559468d2f829d4ccfe885807da06f45319090372c5927494fca417a6e46d54c",
            "a57f1e700ca671a4a3e730a05f32c582577bee7a6eaef7a0fa2a5d53ff8cf85f",
            "01645fb18055f2a547118ad6daf5a376f225acbb1623af71474f3c5cd8515580",
            "78152e9897d998cc2b18bc9e2ab2203d490e47126b93f32d8b728983a7b3f422",
        ]
        self.key = self.keys[0]
        self.base_params = {
            "engine": "google_patents_details",
            "patent_id": "patent/{}/en",
            "api_key": "",
        }
        if test_keys:
            # Test API keys to make sure they still work and remove if any dont before we do anything
            n = len(self.keys) # will change during loop
            to_rm = []
            params = self.base_params
            params["patent_id"] = params["patent_id"].format(TEST_PATENT_ID)

            for i, key in enumerate(self.keys):
                # Do sample request with each to check if they are still valid
                params["api_key"] = key

                search = GoogleSearch(params)
                res = search.get_dict()
                if "error" in res:
                    print(f"API key {i + 1}/{n}: {key} is invalid, removing...")
                    to_rm.append(key)
                    continue
                print(f"API key {i + 1}/{n}: {key} is valid")

            for key in to_rm:
                self.keys.remove(key)
            print(f"Removed {len(to_rm)} invalid API keys")
            self.key = self.keys[0]
            self.next_api_key()

    def next_api_key(self):
        self.key = self.keys[(self.keys.index(self.key) + 1) % len(self.keys)]
        self.base_params['api_key'] = self.key
        return self.key

    def request(self, patent_id):
        try:
            params = self.base_params
            params["patent_id"] = params["patent_id"].format(patent_id)
            retries = 5
            while retries > 0:
                search = GoogleSearch(params)
                results = search.get_dict()
                if 'error' in results:
                    self.next_api_key()
                    retries -= 1
                    continue
                return results
        except:
            return None


CLAIMN = re.compile(r"claim (\d+)")
def is_major(claim: str) -> bool:
    """
    At the moment the best way to test for this is if the first 'part' of the word has "claim %d" in it
        e.g. "The method of claim 1, further..." -> We check for the 'claim x,' part of this.
        otherwise return true (because it's independent)
    :param claim: str claim
    :return:
    """
    # Use regex to check for "claim %d" in the first part of the claim (before the comma)
    # match = re.match(r"claim (\d+),", claim)
    match = CLAIMN.search(claim)
    return match is None # should be true if it's a major claim


"""
TODO update it so that it will handle recursion properly for claims like this one
We have it so that it's relatively simple:
Parent: New sentence, until period, semicolon, or colon.
    If period, end of tree.
    If semicolon, next parent node in tree.
    If colon, go to child in tree.
"""
def sub_claims(claim):
    if ":" in claim:
        parent,children = claim.split(":", 1)
        for child in children.split(":",1)[0].split(";"):
            for sub_claim in sub_claims(child):
                yield parent + sub_claim
    else:
        yield claim

def stringify_claim(claim, prefix=""):
    subclaims = []
    preamble = claim.split(":",1)[0] # always included before each
    prefix = ""
    claim = claim.split(":", 1)[-1]
    for line in claim.split("\n"):
        if ":" in line:
            # New subclaim
            prefix += line
        elif len(line) < 1:
            # Reset back to first level
            prefix = ""
        # else:
        #     elif ";" in line or "." in line:
        else:
            # subclaims.append(preamble + prefix + line)
            subclaims.append(f"{preamble}: {prefix} {line}")
    return subclaims

    # if ":" in claim:
    #     i = claim.index(":")
    #     prefix = claim[:i]
    #     j =
    #     if ":" in claim[i:]:
    #         j = claim[i:].index(":")
    #     for subclaim in claim[i:]


"""
A:
    b;
    c;
    d;
    e:
        f;
        g;
        h.
        
    i:
    


"""

def split_claim(claim) -> list:
    print(list(sub_claims(claim)))
    subclaims = stringify_claim(claim, "")
    elements = claim.split("\n")
    header = remove_numbering(elements[0])
    components = []
    if len(elements) > 2:
        # More sub-elements to split
        # For each one put the previous heading as prefix
        prefix = ""
        for i in range(1, len(elements)-1):
            if ";" not in elements[i]:
                prefix = elements[i]
                continue
            # else ; in elements[i]
            components.append(f"{prefix} {elements[i]}")
    else:
        components = elements[1].split(";")
    return header, components

def is_valid_link(link) -> bool:
    if link != "":
        try:
            page = requests.get(link, timeout=5)
        except:
            page = requests.Response()
            page.status_code = 404
        if page.status_code == 200:
            return True
    return False

CLASSIFICATION_EMOJIS = {
    0: "❌",
    1: "❓",
    2: "✅",
}
def process_claim_t(claim_i, claim, chat, patent_id):
    # Get all components of the claim via newlines, after the header of the claim.
    claim_data_t = []
    header, components = split_claim(claim)
    print(claim_i+1, header)
    for j, component in enumerate(components):
        print(f"\t", j+1, component)
    # component_list = "\n".join([f"* {component}" for component in components])
    component_list = "\n".join([f"* {claim_i+1}.{j+1} {component}" for j,component in enumerate(components)])

    prompt = f"""I am a patent lawyer trying to find products or applications that may be infringing or could use our patent #{patent_id}. This could be produced or distributed by companies, institutes, or other groups of professionals. I need you to provide the top 10 products or applications that match the claim, and an enumeration of each component in the claim to indicate if the match has those components, in a format that follows this outline. Output ONLY an enumerated list of matches, with each entry having the name and a bulleted list of the components it matches. Make sure to include the link! Example:
"1. Google Patents - https://www.patents.google.com
* 1.1. Yes
* 1.2. Yes
* 1.3. Unsure
* 1.4. No"

Do this for the following claim + Components:
{header}
{component_list}"""
    res = chat.ask(prompt)
    for entry in res.split("\n\n"):
        lines = entry.split("\n")
        if len(lines) < len(components):  # should be at least the length + 1 so this is forgiving
            continue
        if len(claim_data_t) == len(components): # should be equal when done dont include any gaff
            return claim_data_t

        name = get_name(lines[0])
        # print("NAME:", name)
        link = get_link(entry)
        # print("LINK:", link)
        classifications = [get_classification(line) for line in lines[1:]]
        # TODO handle when the classifications list is not as long or not matching the length of the components list
        # Check if the entry's link exists
        if is_valid_link(link):
            # Add the data
            claim_data_t.append({"name": name, "link": link, "classifications": classifications})
            print(f"Claim {claim_i + 1} - {name} - {link} -> {classifications}")
    return claim_data_t
    # For each link + name and the claims it appears in
    # claim_data = [[{'name': 'Medtronic StealthStation S8 Surgical Navigation System #2', 'link': 'https://www.medtronic.com', 'classifications': [1, 2, 2, 2, 2]}, {'name': 'Medtronic StealthStation S8 Surgical Navigation System', 'link': 'https://www.medtronic.com', 'classifications': [1, 2, 2, 2, 2]}, {'name': 'Stryker Endoscopy HD Camera System', 'link': 'https://www.stryker.com', 'classifications': [1, 2, 2, 2, 1]}, {'name': 'Karl Storz Endoscopy System', 'link': 'https://www.karlstorz.com', 'classifications': [2, 2, 2, 2, 1]}, {'name': 'Boston Scientific SpyGlass DS Direct Visualization System', 'link': 'https://www.bostonscientific.com', 'classifications': [2, 2, 2, 2, -2]}, {'name': 'Olympus VISERA ELITE II Surgical Imaging System', 'link': 'https://www.olympus-global.com', 'classifications': [1, 2, 2, 2, 1]}, {'name': 'Intuitive Surgical da Vinci Xi Endoscope', 'link': 'https://www.intuitive.com', 'classifications': [-2, 2, 2, 2, -2]}, {'name': 'Richard Wolf Endoscopy System', 'link': 'https://www.richard-wolf.com', 'classifications': [1, 2, 2, 2, 1]}, {'name': 'Fujifilm ELUXEO Endoscopy System', 'link': 'https://www.fujifilm.com', 'classifications': [1, 2, 2, 2, -2]}, {'name': 'CONMED Visualization Systems', 'link': 'https://www.conmed.com', 'classifications': [1, 2, 2, 2, 1]}, {'name': 'Smith Nephew Endoscopy Systems', 'link': 'https://www.smith-nephew.com', 'classifications': [1, 2, 2, 2, -2]}], [], [], [], [], [], [], [], [], [], [], [], [], [{'name': 'Karl Storz Endoscopic DVR System', 'link': 'https://www.karlstorz.com', 'classifications': [2, 2, 2, 2, 2]}, {'name': 'Medtronic METRx System', 'link': 'https://www.medtronic.com', 'classifications': [2, 2, 2, 1, 2]}, {'name': 'Stryker Visuray Endoscopic System', 'link': 'https://www.stryker.com', 'classifications': [2, 2, 2, 2, 2]}, {'name': 'Joimax TESSYS Endoscopic System', 'link': 'https://www.joimax.com', 'classifications': [1, 2, 2, 2, 2]}, {'name': 'Richard Wolf Endoscopic Spine System', 'link': 'https://www.richard-wolf.com', 'classifications': [2, 2, 2, 1, 2]}, {'name': 'Zimmer Biomet Spine Endoscopy', 'link': 'https://www.zimmerbiomet.com', 'classifications': [2, 2, 2, 2, 2]}, {'name': 'Olympus EndoTherapy Systems', 'link': 'https://www.olympusamerica.com', 'classifications': [2, 2, 2, 1, 2]}, {'name': 'Aesculap MiRus Endoscopic System', 'link': 'https://www.aesculap.com', 'classifications': [2, 2, 2, 2, 2]}, {'name': 'Nuvasive Pulse Endoscopy', 'link': 'https://www.nuvasive.com', 'classifications': [1, 2, 2, 2, 2]}], [], [], [], [], [], [{'name': 'Medtronic METRx System', 'link': 'https://www.medtronic.com', 'classifications': [2, 2, 1, 2, 1]}, {'name': 'Stryker Endoscopy Visualization System', 'link': 'https://www.stryker.com', 'classifications': [2, 2, -2, 2, -2]}, {'name': 'NuVasive MAS TLIF System', 'link': 'https://www.nuvasive.com', 'classifications': [2, 2, 1, 2, -2]}, {'name': 'Karl Storz Endoscopy Systems', 'link': 'https://www.karlstorz.com', 'classifications': [2, 2, 1, 2, 1]}, {'name': 'Boston Scientific SpyGlass DS', 'link': 'https://www.bostonscientific.com', 'classifications': [2, 2, -2, 2, -2]}, {'name': 'Richard Wolf Endoscopic Sheaths', 'link': 'https://www.richard-wolf.com', 'classifications': [2, 2, 1, 2, 1]}, {'name': 'Olympus Surgical Endoscopy', 'link': 'https://www.olympus-global.com', 'classifications': [2, 2, -2, 2, -2]}, {'name': 'Zimmer Biomet MIS Spine System', 'link': 'https://www.zimmerbiomet.com', 'classifications': [2, 2, 1, 2, -2]}]]
    # claim_data = [[{'name': 'Medtronic StealthStation S8 Surgical Navigation System', 'link': 'https://www.medtronic.com', 'classifications': [1, 2, 2, 2, 1]}, {'name': 'Stryker 1688 Advanced Imaging Modality System', 'link': 'https://www.stryker.com', 'classifications': [2, 2, 2, 2, 1]}, {'name': 'Karl Storz Endoscopy System', 'link': 'https://www.karlstorz.com', 'classifications': [2, 2, 2, 2, 2]}, {'name': 'Boston Scientific SpyGlass DS Direct Visualization System', 'link': 'https://www.bostonscientific.com', 'classifications': [2, 2, 2, 2, 1]}, {'name': 'Olympus EVIS EXERA III Endoscopy System', 'link': 'https://www.olympusamerica.com', 'classifications': [2, 2, 2, 2, 1]}, {'name': 'Intuitive Surgical da Vinci SP Endoscope', 'link': 'https://www.intuitive.com', 'classifications': [2, 2, 2, 2, 2]}, {'name': 'CONMED EndoSurg Endoscopic System', 'link': 'https://www.conmed.com', 'classifications': [1, 2, 2, 2, 1]}, {'name': 'Richard Wolf Endoscopy System', 'link': 'https://www.richard-wolf.com', 'classifications': [2, 2, 2, 2, 1]}, {'name': 'Fujifilm ELUXEO Endoscopy System', 'link': 'https://www.fujifilm.com', 'classifications': [1, 2, 2, 2, 0]}, {'name': 'Cook Medical Endoscopic Access Devices', 'link': 'https://www.cookmedical.com', 'classifications': [2, 2, 2, 1, 1]}], [], [], [], [], [], [], [], [], [], [], [], [], [{'name': 'Joimax TESSYS Endoscopic System', 'link': 'https://www.joimax.com/tessys', 'classifications': [1, 2, 2, 0, 0]}, {'name': 'NuVasive s LessRay System', 'link': 'https://www.nuvasive.com/lessray', 'classifications': [0, 2, 0, 0, 0]}, {'name': 'Karl Storz Endoscopic Spine System', 'link': 'https://www.karlstorz.com/spine', 'classifications': [2, 2, 2, 1, 1]}], [], [], [], [], [], [{'name': 'Medtronic METRx System', 'link': 'https://www.medtronic.com', 'classifications': [2, 2, 1, 2, 0]}, {'name': 'Stryker Endoscopy Visualization System', 'link': 'https://www.stryker.com', 'classifications': [2, 2, 1, 2, 0]}, {'name': 'Boston Scientific SpyGlass DS', 'link': 'https://www.bostonscientific.com', 'classifications': [2, 2, 0, 2, 0]}, {'name': 'Olympus EndoTherapy Devices', 'link': 'https://www.olympusamerica.com', 'classifications': [2, 2, 0, 2, 0]}, {'name': 'Karl Storz Endoscopy Systems', 'link': 'https://www.karlstorz.com', 'classifications': [2, 2, 1, 2, 0]}, {'name': 'NuVasive MAS TLIF System', 'link': 'https://www.nuvasive.com', 'classifications': [2, 2, 2, 2, 1]}, {'name': 'Richard Wolf Endoscopes', 'link': 'https://www.richard-wolf.com', 'classifications': [2, 2, 0, 2, 0]}, {'name': 'Zimmer Biomet Spine Devices', 'link': 'https://www.zimmerbiomet.com', 'classifications': [2, 2, 2, 2, 1]}]]



chat = ChatGPT(model="deepseek-chat")
def patentate(patent_id):
    SERPAPI = SerpApi()
    data = SERPAPI.request(TEST_PATENT_ID)
    title = gwd(data, ['title'])
    pubdate = gwd(data, ['publication_date'])
    claims = gwd(data, ['claims'])
    similar_documents = gwd(data, ['similar_documents'])
    # list of claim results, each claim has results and each result has name, description, link.
    claim_data = [[] for _ in range(len(claims))] # list of list of dictionaries with name, description, link {"name": "", "link": "", "classifications": ""}
    threads = []
    results = [None] * len(claims) # list of results for each claim
    # TODO generalize this
    def thread_caller(result_i, func, *args):
        # Call the function with the provided arguments in a thread and put it's return value in results array
        results[result_i] = func(*args)

    for claim_i, claim in enumerate(claims):
        split_claim(claim)
        if not is_major(claim):
            # skip
            continue
        thread = threading.Thread(target=thread_caller, args=(claim_i, process_claim_t, *(claim_i, claim, chat,patent_id)))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Combine results back
    for claim_i, claim in enumerate(claims):
        if not is_major(claim):
            # skip
            continue
        claim_data[claim_i] = results[claim_i]
        # claim_data[claim_i] = process_claim_t(claim_i, claim)


    matches = {}
    scores = {}
    # meta = {}
    for claim_i, claim in enumerate(claim_data):
        for entry in claim:
            if entry["link"] not in matches:
                matches[entry["link"]] = {}
            if claim_i + 1 not in matches[entry["link"]]:
                matches[entry["link"]][claim_i + 1] = {}

            # There could be multiple products by one company that match a claim, so we have another dict here
            matches[entry["link"]][claim_i + 1][entry["name"]] = entry["classifications"]

    # for match in
    for link, claim_indices in matches.items():
        # matches[link]["score"] = 0
        scores[link] = 0
        # Score is total number generated by adding all it's classifications together.
        # TODO SHOULD UNKNOWN BE 0.5 INSTEAD OF 0 AND NEGATIVE BE 0 INSTEAD OF -1 ???
        for claim_i, products in claim_indices.items():
            for product_name, product_classifications in products.items():
                # matches[link]["score"] += sum(product_classifications)
                score = sum(product_classifications)
                if score == len(product_classifications)*2:
                    # Complete match, add a bonus amplifier to boost this score
                    score += 100
                scores[link] += score

    # Now iterate by score and make our big result list
    i = 1
    for link, claim_indices in sorted(matches.items(), key=lambda x: scores[x[0]], reverse=True):
        # print(f"Link: {link}, Claims: {claim_indices}, Name: {meta[link]['name']}, Description: {meta[link]['description']}")
        print(f"{i}. {link}, Score {scores[link]}")
        for claim_i, products in claim_indices.items():
            header,components = split_claim(claims[claim_i-1])
            print(f"\tClaim {claim_i}: \"{header}\"")
            for product_name, product_classifications in products.items():
                print(f"\t\tProduct: {product_name}")
                print(f"\t\tSub-Claim Matches:")
                for component_i, classification in enumerate(product_classifications):
                    s = components[component_i][:100]
                    if len(components[component_i]) > 100:
                        s = components[component_i][:100].strip() + "..."
                    print(f"\t\t\t{CLASSIFICATION_EMOJIS[classification]} \"{s}\"")

        # for claim_i in claim_indices:
        #     print(f"Claim {claim_i + 1}: {claims[claim_i]}")
        # print("\n")
        print()
        i += 1
#
# print(data)
# TEST_PATENT_ID = "US20230027590A1"
TEST_PATENT_ID = "US10729277B2"
# TEST_PATENT_ID = "US9687142B1"
patentate(TEST_PATENT_ID)
# "6328b60d23198d8e3ef25bad85cc2760b9b3fa4de8a83bdb0bfc0fc124714dcd"
# params = {
#     "engine": "google_patents_details",
#     "patent_id": "patent/US20230027590A1/en",
#     "api_key": "secret_api_key"
# }
#
# search = GoogleSearch(params)
# results = search.get_dict()

"""
list of companies as the overlap points of each of the products recommended
    e.g. nest - thermostat 4.3
    e.g.2 nest - security camera


list of each product and the parts that it overlaps the claim

For each claim - url of PRODUCT
    for each component
        are they present in the product?

post-process check if URL is real

output format for the finale

# for each claim:
# print the claim, sort results by most positive matches (just sum the classifications b/c numbering system)
# 
# CLAIM 1 - SOMETHING IMPORTANT
#     1: Richard Wolf Endoscopy System (https://www.richard-wolf.com) - Sub Claim Results: 3/5 positive matches, 2/5 possible matches, 0/5 negative matches
#     2: Intuitive Surgical da Vinci Xi Endoscope (https://www.intuitive.com) - 

OUTPUT FORMAT AS CONFIRMED BY BRYCE
print by company:
    each one in collapsible section, ordered by highest total
    for each section under the company, we do it similar to how we have it here (pog)
    
have a cool updating checkbox as we get each claim

"""