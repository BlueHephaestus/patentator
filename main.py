"""


"""
import re
from serpapi import GoogleSearch
# CoinGecko
from utils.ai_utils import *
import requests

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
    return None

def get_classification(line):
    classification = clean(remove_numbering(outside(line)))
    if classification.lower() == "yes":
        return "Y"
    elif classification.lower() == "no":
        return "N"
    return "U" # unknown / unsure

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


CLAIMN = re.compile(r"claim (\d+),")
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

def split_claim(claim) -> list:
    header = claim.split("\n")[0]
    components = claim.split("\n")[1:]
    return header, components


chat = ChatGPT(model="deepseek-chat")
def patentate(patent_id):
    SERPAPI = SerpApi()
    data = SERPAPI.request(TEST_PATENT_ID)
    title = gwd(data, ['title'])
    pubdate = gwd(data, ['publication_date'])
    claims = gwd(data, ['claims'])
    similar_documents = gwd(data, ['similar_documents'])
    # list of claim results, each claim has results and each result has name, description, link.
    claim_data = [[] for _ in range(len(claims))] # list of list of dictionaries with name, description, link {"name": "", "description": "", "link": ""}
    for claim_i, claim in enumerate(claims):
        if not is_major(claim):
            # skip
            continue
        # Get all components of the claim via newlines, after the header of the claim.
        header, components = split_claim(claim)
        print(claim_i+1, header)
        for j, component in enumerate(components):
            print(f"\t", j+1, component)
        # component_list = "\n".join([f"* {component}" for component in components])
        component_list = "\n".join([f"* {claim_i+1}.{j+1} {component}" for j,component in enumerate(components)])

        # if claim_i in [0, 13, 19]:

        prompt = f"""I am a patent lawyer trying to find applications that may be infringing or could use our patent # {patent_id}. This could include companies, institutes, or other groups of professionals. I need you to provide the top 10 companies or application descriptions that follow this outline. Output ONLY an enumerated list of matches, with 3 lines each - Name, Description, and Link. Example:\n"1. Name: Google Patents\nDescription: A patent resource for viewing and understanding patents and plenty of details regarding them.\nLink: https://www.patents.google.com".\n\n{claim}"""
        prompt = f"""I am a patent lawyer trying to find products or applications that may be infringing or could use our patent #{patent_id}. This could be produced or distributed by companies, institutes, or other groups of professionals. I need you to provide the top 10 products or applications that match the claim, and an enumeration of each component in the claim to indicate if the match has those components, in a format that follows this outline. Output ONLY an enumerated list of matches, with each entry having the name and a bulleted list of the components it matches. Make sure to include the link! Example:
"1. Name: Google Patents - https://www.patents.google.com
* Component 1, an online database: Yes
* Component 2, a search interface: Yes
* Component 3, A online discussion forum: Unsure
* Component 4, a sentiment analysis system: No"

Do this for the following claim + Components:
{header}
{component_list}"""
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

            name = get_name(lines[0])
            print("NAME:", name)
            link = get_link(entry)
            print("LINK:", link)
            for line in lines[1:]:
                print("\tCLASS:", get_classification(line))
#         # TODO ADD ERROR REDUNDANCY HERE
#         for entry in res.split("\n\n"):
#             name, desc, link = entry.split("\n")
#             name = name.split(": ", 1)[1].strip()
#             desc = desc.split(": ", 1)[1].strip()
#             link = link.split(": ", 1)[1].strip()
#             try:
#                 page = requests.get(link, timeout=5)
#             except:
#                 page = requests.Response()
#                 page.status_code = 404
#             if page.status_code == 200:
#                 claim_data[claim_i].append({"name": name, "description": desc, "link": link})
#                 print(f"Claim {claim_i + 1} - {name} - {link}")
#
#     # For each link + name and the claims it appears in
#     matches = {}
#     meta = {}
#     for claim_i, claim in enumerate(claim_data):
#         for entry in claim:
#             if entry["link"] not in matches:
#                 matches[entry["link"]] = []
#
#             if entry["link"] not in meta:
#                 meta[entry["link"]] = entry
#
#             matches[entry["link"]].append(claim_i+1)
#
#     for link, claim_indices in sorted(matches.items(), key=lambda x: len(x[1]), reverse=True):
#         print(f"Link: {link}, Claims: {claim_indices}, Name: {meta[link]['name']}, Description: {meta[link]['description']}")
#         # for claim_i in claim_indices:
#         #     print(f"Claim {claim_i + 1}: {claims[claim_i]}")
#         # print("\n")
#
# print(data)
# TEST_PATENT_ID = "US9687142B1"
TEST_PATENT_ID = "US9687142B1"
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

"""