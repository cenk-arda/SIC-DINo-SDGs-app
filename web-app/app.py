import os
from flask import Flask, current_app, render_template, request, jsonify
from load_evaluate_model import predict_text, load_model

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        try:
            sentence = request.form["text"]
            """if input is empty or not a string or less than 10 words or greater than 512 words, return error"""
            if not sentence or not isinstance(sentence, str) or len(sentence.split()) < 10 or len(
                    sentence.split()) > 512:
                return jsonify({"error": "Your input must be a string with at least 10 words and at most 512 words."})

            softmax_probabilities, label = predict_text(sentence, current_app.model)
            """make softmax probabilities a list of dictionaries"""
            softmax_probabilities = softmax_probabilities.tolist()
            softmax_probabilities = [{"sdg": i + 1, "probability": softmax_probabilities[0][i]} for i in
                                     range(len(softmax_probabilities[0]))]
            """since label is from 0 to 14, we need to add 1 to get the correct label"""
            assert label is not None
            label = label + 1
            int_label = int(label)
            """Sustainable development goals as a dictionary of strings"""
            sdg_dict = {
                "01": "No Poverty",
                "02": "Zero Hunger",
                "03": "Good Health and Well-Being",
                "04": "Quality Education",
                "05": "Gender Equality",
                "06": "Clean Water and Sanitation",
                "07": "Affordable and Clean Energy",
                "08": "Decent Work and Economic Growth",
                "09": "Industry, Innovation and Infrastructure",
                "10": "Reduced Inequalities",
                "11": "Sustainable Cities and Communities",
                "12": "Responsible Consumption and Production",
                "13": "Climate Action",
                "14": "Life Below Water",
                "15": "Life On Land",
                "16": "Peace, Justice and Strong Institutions",
                "17": "Partnerships for the Goals",
            }

            """ add a zero to the label if it is less than 10 """
            if label < 10:
                label = "0" + str(label)
            else:
                label = str(label)

            sdg_description = "This is a description of the SDG"

            result = {
                "sdg": int_label,
                "sdg_description": sdg_description,
                "sdg_name": sdg_dict[label],
                "softmax_probabilities": softmax_probabilities,
                "sentence": sentence,
            }
            return jsonify(result)

        except AssertionError as e:
            return jsonify({"error": str(e) + " We couldn't find any SDGs related with your input."})
        except Exception as e:
            return jsonify({"error": str(e)})


if __name__ == '__main__':
    with app.app_context():
        current_app.model = load_model()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
