from flask import Flask, render_template, request
from symptoms_data import symptoms_dict

app = Flask(__name__)

def predict(symptoms):
    symptoms = set(symptoms)

    if {"fever", "cough", "fatigue"}.issubset(symptoms):
        return "🤒 High chance of flu-like infection."
    elif {"headache", "fatigue"}.issubset(symptoms):
        return "🧠 Possible stress-related headache or migraine."
    elif {"cold", "cough"}.issubset(symptoms):
        return "🤧 Common cold likely."
    else:
        return "⚠️ Insufficient symptom combination for a clear prediction. Monitor and consider professional care."

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    detailed = ""

    if request.method == "POST":
        user_symptom = request.form.get("symptom", "").strip().lower()

        if user_symptom:
            advice = symptoms_dict.get(user_symptom)
            if advice:
                result = f"✅ Symptom recognized: {user_symptom.capitalize()}"
                detailed = advice
            else:
                # If user entered a combined/multi-symptom string separated by commas,
                # reuse existing simple prediction logic
                symptom_list = [s.strip().lower() for s in user_symptom.split(",") if s.strip()]
                if symptom_list:
                    result = predict(symptom_list)
                    detailed = "Try a nearby clinic if symptoms continue or worsen."
                else:
                    result = "Please enter a valid symptom."
        else:
            result = "Please enter a symptom to continue."

    return render_template("index.html", result=result, detailed=detailed)

if __name__ == "__main__":
    app.run(debug=True)
