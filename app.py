import os

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
from flask_socketio import SocketIO

import os
import json
from dotenv import load_dotenv
# Add Azure OpenAI package


app = Flask(__name__)




with app.app_context():
    foo = "bar"


@app.route('/')
def index():
   print('Request for index page received')
   cache['foo'] = 0
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   question = request.form.get('question')

   if name:
       print('This is the question: %s' % question)
       return render_template('answer.html', answer = question)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))



@app.route('/api/ping')
def getApiPing():
    return "API is sasss"





@app.route('/chat')
@app.route('/chat', methods=['POST'])
def showChat():
    return render_template('aichat.html')

@app.route('/api/getAnswerFromAi2', methods=['POST'])
def getAnswerFromAi():
        load_dotenv()
        azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
        azure_oai_key = os.getenv("AZURE_OAI_KEY")
        azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")
        azure_search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        azure_search_key = os.getenv("AZURE_SEARCH_KEY")
        azure_search_index = os.getenv("AZURE_SEARCH_INDEX")

        # Initialize the Azure OpenAI client
        client = AzureOpenAI(
            base_url=f"{azure_oai_endpoint}/openai/deployments/{azure_oai_deployment}/extensions",
            api_key=azure_oai_key,
            api_version="2023-09-01-preview")

        print(client)

        question = request.form.get('text')

        extension_config = dict(dataSources=[
            {
                "type": "AzureCognitiveSearch",
                "parameters": {
                    "endpoint": azure_search_endpoint,
                    "key": azure_search_key,
                    "indexName": azure_search_index,
                }
            }]
        )

        response = client.chat.completions.create(
            model=azure_oai_deployment,
            temperature=0.5,
            max_tokens=500,
            messages=[
                {"role": "system", "content": "Du er en DFØ agent og kan alt om økonomi i offentlig sektor. Du skal svare bassert på data du har på best måte mulig og på norsk"},
                {"role": "user", "content": question}
            ],
            extra_body=extension_config
        )

        return  response.choices[0].message.content


@app.route('/api/getAnswerFromAi', methods=['POST'])
def getAnswerFromAiWithReq():
        import requests
        import json
        load_dotenv()
        azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
        azure_oai_key = os.getenv("AZURE_OAI_KEY")
        azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")
        azure_search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        azure_search_key = os.getenv("AZURE_SEARCH_KEY")
        azure_search_index = os.getenv("AZURE_SEARCH_INDEX")

        url = f"{azure_oai_endpoint}/openai/deployments/{azure_oai_deployment}/extensions/chat/completions?api-version=2023-06-01-preview"
        question = request.form.get('text')
        payload = json.dumps({
            "temperature": 0.5,
            "max_tokens": 1000,
            "top_p": 1,
            "dataSources": [
                {
                    "type": "AzureCognitiveSearch",
                    "parameters": {
                        "endpoint": f"{azure_search_endpoint}",
                        "key": f"{azure_search_key}",
                        "indexName": f"{azure_search_index}",
                        "roleInformation": "Eres un asistente de cocinas Buraglia y tienes conocimientos tecnicos de los productos. Debes responder en español y al final de la respuesta agregar el nombre del archivo y la pagina donde se encuentra la referencia. Contesta en el idioma de la pregunta."
                    }
                }
            ],
            "messages": [
                {"role": "system", "content": "Eres un asistente de cocinas Buraglia y tienes conocimientos tecnicos de los productos. Debes responder en español y al final de la respuesta agregar el nombre del archivo y la pagina donde se encuentra la referencia. Contesta en el idioma de la pregunta."},
                {"role": "user","content":f"'{question}'"}
            ]
        })
        headers = {
            'Content-Type': 'application/json',
            'api-key': f"{azure_oai_key}"
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        resp = response.json()
        return resp["choices"][0]["messages"][1]["content"]



if __name__ == '__main__':
    app.run(
        debug=True, passthrough_errors=True,
        use_debugger=False, use_reloader=True
    )
