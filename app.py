import requests
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

# user_input = input("Enter the description: ")
user_input = "Feeling a pain in the chest on the top part of the body"

user_emb = model.encode(user_input)

symptom_name = "chest%20pain"
get_request = "http://localhost:8080/MAIN/concepts/?term={symptom_name}"
response = requests.get(get_request.format(symptom_name=symptom_name))

data = response.json()

max_score = 0
max_score_concept = None
max_score_description = None

for concept in data['items']:
    concept_id = concept['conceptId']
    description = concept['fsn']['term']

    concept_emb = model.encode(description)

    cosine_scores = util.pytorch_cos_sim(user_emb, concept_emb)

    print("Sentence: ", description, "\nSimilarity: ", cosine_scores.item(), "\n")

    if cosine_scores.item() > max_score:
        max_score = cosine_scores.item()
        max_score_concept = concept_id
        max_score_description = description

print("User input: ", user_input)
print("Most similar concept: ", max_score_concept, "\nDescription: ", max_score_description, "\nSimilarity: ", max_score)

# Add CSS for styling
components.html('''
<style>
h1, h2, h3, h4, h5, h6 {
    color: #303f9f !important;
    font-family: 'Arial', sans-serif;
}

body {
    padding: 20px;
}

.card {
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin-bottom: 20px;
}

.card-title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 10px;
}

.card-content {
    font-size: 16px;
    margin-bottom: 10px;
}

hr {
    border: none;
    border-top: 1px solid #ccc;
    margin: 20px 0;
}

</style>
''')
