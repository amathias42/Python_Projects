import requests  # pylint: disable=import-error

HEADERS = {
    "authorization": "Basic T09JQVBJLTM4NFhST0RaVVk5UVdLOlRFTVAtVE9LRU4tQ0RMTEExVVlIR0dKUFc="
}

startTime = "2023-02-20T16:32:15.000Z"
endTime = "2023-02-24T16:32:15.000Z"

def makeReqURL (startTime, endTime):
    return (
    "https://ooinet.oceanobservatories.org/api/m2m/12576/sensor/inv/RS01SBPS/SF01A/00-ENG/streamed/secondary_node_eng_data?beginDT="
    + startTime
    + "&endDT="
    + endTime
    + "&limit=1000&parameters=7017,7018,7&require_deployment=False"
)

url = (
    "https://ooinet.oceanobservatories.org/api/m2m/12576/sensor/inv/RS01SBPS/SF01A/00-ENG/streamed/secondary_node_eng_data?beginDT="
    + startTime
    + "&endDT="
    + endTime
    + "&limit=1000&parameters=7017,7018,7&require_deployment=False"
)
payload = ""

response = requests.request("GET", url, data=payload, headers=HEADERS)
print(response.text)
