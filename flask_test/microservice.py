from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api', methods=['GET','POST'])
def api_endpoint():
    data = request.json
    response = {'message': 'Request received', 'data': data}
    return jsonify(response)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=7000)

