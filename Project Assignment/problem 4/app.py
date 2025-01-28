from flask import Flask, render_template, request
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Sample dataset of content items with tags
content_items = [
    {"id": 1, "title": "Movie A", "tags": ["action", "adventure"]},
    {"id": 2, "title": "Movie B", "tags": ["comedy", "romance"]},
    {"id": 3, "title": "Movie C", "tags": ["action", "thriller"]},
    {"id": 4, "title": "Movie D", "tags": ["comedy", "action"]},
    {"id": 5, "title": "Movie E", "tags": ["romance", "drama"]},
]

# Convert tags to a binary matrix for similarity calculation
tags = list(set(tag for item in content_items for tag in item["tags"]))
content_matrix = np.zeros((len(content_items), len(tags)))

for i, item in enumerate(content_items):
    for tag in item["tags"]:
        content_matrix[i, tags.index(tag)] = 1

def recommend_content(user_preferences):
    user_vector = np.zeros(len(tags))
    for tag in user_preferences:
        if tag in tags:
            user_vector[tags.index(tag)] = 1

    similarities = cosine_similarity([user_vector], content_matrix)
    recommended_indices = np.argsort(similarities[0])[::-1]
    recommended_content = [content_items[i] for i in recommended_indices]

    return recommended_content

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_preferences = request.form.getlist("preferences")
        recommendations = recommend_content(user_preferences)
        return render_template("index.html", recommendations=recommendations, tags=tags)
    return render_template("index.html", recommendations=None, tags=tags)

if __name__ == "__main__":
    app.run(debug=True)