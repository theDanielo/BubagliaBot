import requests
import json

url = "https://integrate-azure-openai-into-app.openai.azure.com/openai/deployments/ownDataInDeployment/extensions/chat/completions?api-version=2023-06-01-preview"

payload = json.dumps({
  "temperature": 0.5,
  "max_tokens": 1000,
  "top_p": 1,
  "dataSources": [
    {
      "type": "AzureCognitiveSearch",
      "parameters": {
        "endpoint": "https://dg-searchservice-b.search.windows.net",
        "key": "huubhSBvFCQF2B0SUB6T7KD59i1jw8h19XdON6XRmFAzSeApbIkW",
        "indexName": "dfo-srs-index"
      }
    }
  ],
  "messages": [
    {
      "role": "user",
      "content": "Kan du oppsumere SRS-17?"
    }
  ]
})
headers = {
  'Content-Type': 'application/json',
  'api-key': '61cb68db286549ad86175abc0b42f60b'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
