import hmac
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

github_secret = 'thu-lost-and-found'

def encryption(data):
    key = github_secret.encode('utf-8')
    obj = hmac.new(key, msg=data, digestmod='sha256')
    return obj.hexdigest()

@app.route('/lost_and_found_hook', methods=['POST'])
def post_data():
    post_data = request.data
    token = encryption(post_data)
    signature = request.headers.get('X-Hub-Signature-256', '').split('=')[-1]
    if signature != token:
        return "token error", 401
    if request.json['ref'] == 'refs/heads/master':
        os.system('sh deploy.sh')
    return jsonify({"status": 200})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8989)
