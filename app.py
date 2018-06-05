from flask import Flask,abort,jsonify,make_response,request, url_for
from flasgger import Swagger
import logging
import json
import datetime
import classify as spamClassifier

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

app = Flask(__name__,static_folder=None)
app.config['SWAGGER'] = {
    'title': 'SMS Classifier',
    'description': 'multinomial naive-bayes classifier for spam SMS messages',
    'version' : "0.1.0",
    'contact' : {
       'email' : 'jbslanka@ncsu.edu',
       'name'  : 'John Slankas',
       'url'   : 'http://www.slankas.net'
    }
}
swagger = Swagger(app)


@app.route('/')
def showRoutes():
    """
    Get Route Info
    Return all of the defined routes with their associated docstrings
    ---
    tags:
      - routes
    parameters: {}
    responses:
      200:
        description: listing of the endpoints in JSON
        schema:
          type: object
          properties:
            code:
              type: string
              description: http response code
            endpoints:
              type: array
              items:
                type: object
                properties:
                  rule:
                    type: string
                  methods:
                    type: string
                  docString:
                    type: string
    """
    routes = []
    for rule in app.url_map.iter_rules():
        print (rule)
        print (type(rule))
        print (rule.endpoint)
        myRule = {}
        myRule["rule"] = rule.rule
        myRule["methods"] = ",".join(list(rule.methods))

        if rule.endpoint != 'static':
            if hasattr(app.view_functions[rule.endpoint], 'import_name'):
                import_name = app.view_functions[rule.endpoint].import_name
                obj = import_string(import_name)
                myRule["docString"] = obj.__doc__
            else:
                myRule["docString"] =  app.view_functions[rule.endpoint].__doc__

        routes.append(myRule)

    return jsonify(code=200, endPoints=routes)

@app.route('/v1/classifySMS',methods=['POST'])
def getSpamOrHam():
    """
    Classify SMS

    Determines whether or not the pass text attribute is spam or ham
    ---
    tags:
      - classifier
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - name: body
        in: body
        description: request body
        required: true
        schema:
          type: object
          required: 
            - text
          properties:
            text:
              description: message to classifiy 
              type: string
    responses:
      200:
        description: was the message ham or spam
        schema:
          type: object
          properties:
            result:
              description: ham, spam
              type: string
    """
    contentJSON = request.json
    answer = spamClassifier.makePrediction(contentJSON["text"])
    result = { "result" : answer }
    return jsonify(result)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

