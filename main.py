from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/find-sports-fields', methods=['GET'])
def get_businesses():
    #Get the queries from the url being sent from frontend
    location = request.args.get('location')
    sorting = request.args.get('option')

    #Keep API key in a .env file for security, if it's not found then send a 500 error message
    yelp_api_key = os.getenv("YELP_API_KEY")
    if not yelp_api_key:
        return jsonify({"error": "Yelp API key not provided"}), 500

    #Yelp API with authorization
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {'Authorization': f'Bearer {yelp_api_key}'}
    params = {"location": location, "term": "sports fields and facilities", "option": sorting,}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        else:
            return jsonify({"error": "Failed to fetch data from Yelp API"}), response.status_code
    except Exception as e:
        return jsonify({"error": f"Error making request to Yelp API: {e}"}), 500

#Host frontend page
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT"))
