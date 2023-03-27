import werkzeug.exceptions
from dotenv import load_dotenv

from resolve_query_from_hyperlink import fetch_answer

load_dotenv()
from flask import Flask, request

app = Flask(__name__)


@app.errorhandler(werkzeug.exceptions.BadRequest)
@app.route('/fetch', methods=['GET'])
def fetch():
    json_body = request.get_json()
    url = json_body.get('url', None)
    query = json_body.get('query', None)

    if url is None:
        return 'url is required', 400

    if query is None:
        return 'query is required', 400

    # setting cleanup to True will always download regardless of previous caching
    ans = fetch_answer(url, query, cleanup=False)
    return {'openai_response': ans}


app.run(host='0.0.0.0', port=8000)
