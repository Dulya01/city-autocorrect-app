from flask import Flask, request, jsonify
from flask_cors import CORS
from rapidfuzz import process
import requests

app = Flask(__name__)
CORS(app)

GOOGLE_API_KEY = "AIzaSyDn0h7IDz-OjoTu_1HqpWIav5dRMzEjKGw"

cities = [
    "Colombo", "Kandy", "Galle", "Jaffna", "Negombo",
    "Anuradhapura", "Trincomalee", "Batticaloa", "Matara",
    "Ratnapura", "Kurunegala", "Badulla", "Polonnaruwa"
]

def get_city_info(city_name):
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        "input": city_name,
        "inputtype": "textquery",
        "fields": "formatted_address,name,geometry",
        "key": GOOGLE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    print("Google API Response:", data)  # DEBUG LOG
    if data.get("candidates"):
        return data["candidates"][0]
    return None

@app.route("/correct-city", methods=["POST"])
def correct_city():
    data = request.json
    user_input = data.get("city", "")
    print(f"User input: {user_input}")  # DEBUG LOG

    match = process.extractOne(user_input, cities)
    print(f"Match result: {match}")  # DEBUG LOG

    if match and match[1] >= 60:  # Lowered from 80 to 60 for flexibility
        corrected_city = match[0]
        city_info = get_city_info(corrected_city)
        if city_info:
            return jsonify({
                "corrected_city": corrected_city,
                "details": city_info
            })
        else:
            return jsonify({
                "corrected_city": corrected_city,
                "details": "No detailed info found from Google API."
            })
    else:
        return jsonify({"error": "City not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)

