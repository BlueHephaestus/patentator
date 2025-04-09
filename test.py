# Use an API to get the current patent information when providing a patent number
def get_patent_info(patent_number):
    import requests
    import json
    # url = f"https://api.patentsview.org/patents/query?q={\"patent_number\":\"{patent_number}\"}"
    url = f"https://api.patentsview.org/patents/query?q={{\"patent_number\":\"{patent_number}\"}}"
    response = requests.get(url)
    data = json.loads(response.text)
    return data
print(get_patent_info("20230027590A1"))
# print(get_patent_info("US20180000001A1")["patents"][0]["patent_title"])