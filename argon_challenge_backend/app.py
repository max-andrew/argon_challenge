from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

# Import the synonyms list
from synonyms import NSCLC_SYNONYMS

app = Flask(__name__)

# Update CORS configuration to allow requests from frontend origin
CORS(app, resources={
    r"/search": {
        "origins": "*",
        "methods": ["GET", "OPTIONS"],
    }
})

# Load the JSON dataset
def load_dataset(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset file '{file_path}' not found.")
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON: {e}")

# Normalize disease terms in a single entry
def normalize_disease(disease_text):
    if not isinstance(disease_text, str):
        return ""
    disease_text = disease_text.lower()
    for synonym in NSCLC_SYNONYMS:
        if synonym.lower() in disease_text:
            return "non small cell lung cancer"
    return disease_text

# Preprocess the dataset
def preprocess_dataset(data):
    for i, entry in enumerate(data):
        # Extract disease information
        conditions_module = entry.get('protocolSection', {}).get('conditionsModule', {})
        conditions = conditions_module.get('conditionList', {}).get('condition', [])
        if not conditions:
            conditions = conditions_module.get('conditions', [])
        print(f"Trial {i}: conditions = {conditions}")
        if conditions:
            # Join multiple conditions into a single string
            entry['disease'] = '; '.join(conditions)
            entry['normalized_disease'] = normalize_disease(entry['disease'])
        else:
            entry['disease'] = ''
            entry['normalized_disease'] = ''
            print(f"Trial {i}: No conditions found.")

        # Extract title information
        identification_module = entry.get('protocolSection', {}).get('identificationModule', {})
        title = identification_module.get('officialTitle', '') or identification_module.get('briefTitle', '')
        print(f"Trial {i}: title = {title}")
        entry['title'] = title

        # Extract therapy information if available
        interventions_module = entry.get('protocolSection', {}).get('interventionsModule', {})
        interventions = interventions_module.get('interventionList', {}).get('intervention', [])
        print(f"Trial {i}: interventions = {interventions}")
        therapies = []
        for intervention in interventions:
            intervention_name = intervention.get('interventionName', '')
            if intervention_name:
                therapies.append(intervention_name)
        entry['therapy'] = '; '.join(therapies)
        print(f"Trial {i}: therapy = {entry['therapy']}")
    return data

# Load and preprocess the dataset at startup
DATASET_PATH = 'ctg-studies.json' 
try:
    clinical_trials = load_dataset(DATASET_PATH)
    clinical_trials = preprocess_dataset(clinical_trials)
    print(f"Loaded {len(clinical_trials)} clinical trials.")
except Exception as e:
    print(f"Error loading dataset: {e}")
    clinical_trials = []

# Define the search endpoint
@app.route('/search', methods=['GET'])
def search_trials():
    disease_query = request.args.get('disease', '').strip().lower()
    therapy_query = request.args.get('therapy', '').strip().lower()

    # Initialize filtered list
    filtered_trials = clinical_trials

    # Filter by disease if query is provided
    if disease_query:
        # Check if the disease query matches any NSCLC synonym
        if disease_query in [syn.lower() for syn in NSCLC_SYNONYMS]:
            normalized_query = "non small cell lung cancer"
            filtered_trials = [trial for trial in filtered_trials if trial.get('normalized_disease') == normalized_query]
        else:
            # For other diseases, perform a case-insensitive substring match
            filtered_trials = [
                trial for trial in filtered_trials
                if trial.get('normalized_disease') and disease_query in trial['normalized_disease'].lower()
            ]

    # Further filter by therapy if query is provided
    if therapy_query:
        filtered_trials = [
            trial for trial in filtered_trials
            if 'therapy' in trial and therapy_query in trial['therapy'].lower()
        ]

    # Extract titles of the filtered trials
    titles = [trial.get('title', 'No Title Provided') for trial in filtered_trials]

    return jsonify(titles)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
