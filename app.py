from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "name": "Handmade Soy Candle", "category": "Home Decor", "price": 399, "tags": ["home", "gift", "relaxation"], "description": "A handcrafted scented soy candle for a calm home atmosphere."},
    {"id": 2, "name": "Organic Cotton Tote Bag", "category": "Fashion", "price": 299, "tags": ["fashion", "eco", "daily"], "description": "Reusable organic cotton tote bag for everyday shopping."},
    {"id": 3, "name": "Handmade Ceramic Mug", "category": "Kitchen", "price": 449, "tags": ["kitchen", "gift", "coffee"], "description": "A unique handmade ceramic mug for coffee and tea lovers."},
    {"id": 4, "name": "Natural Skincare Gift Box", "category": "Beauty", "price": 799, "tags": ["beauty", "gift", "natural"], "description": "A curated box containing natural handmade skincare essentials."},
    {"id": 5, "name": "Macrame Wall Hanging", "category": "Home Decor", "price": 699, "tags": ["home", "decor", "gift"], "description": "Handcrafted macrame decoration for bedrooms and living rooms."},
    {"id": 6, "name": "Personalized Notebook", "category": "Stationery", "price": 349, "tags": ["stationery", "study", "gift"], "description": "A customizable notebook suitable for students and professionals."},
]

def recommend(query):
    q = query.lower().strip()
    words = set(q.split())
    scored = []
    for p in PRODUCTS:
        score = 0
        searchable = (p["name"] + " " + p["category"] + " " + p["description"] + " " + " ".join(p["tags"])).lower()
        for word in words:
            if len(word) > 2 and word in searchable:
                score += 2
        for tag in p["tags"]:
            if tag in q:
                score += 3
        if "under 500" in q and p["price"] <= 500:
            score += 4
        if "under 1000" in q and p["price"] <= 1000:
            score += 2
        if score:
            scored.append((score, p))
    scored.sort(key=lambda x: (-x[0], x[1]["price"]))
    return [p for _, p in scored[:4]] or PRODUCTS[:4]

def assistant_reply(message):
    q = message.lower()
    if any(x in q for x in ["hello", "hi", "hey"]):
        return "Hi! I can help you discover products, compare options, and find recommendations based on your needs."
    if "gift" in q:
        return "For a gift, I recommend the Handmade Ceramic Mug, Natural Skincare Gift Box, or Personalized Notebook."
    if "under 500" in q:
        return "Here are some good options under ₹500. I focused on useful handmade products with good gifting potential."
    if "home" in q or "decor" in q:
        return "For home decor, try the Handmade Soy Candle or Macrame Wall Hanging."
    if "student" in q or "study" in q:
        return "For students, the Personalized Notebook is a practical choice."
    return "I found some products that match your request. You can refine your search with words like gift, home, student, beauty, or a budget such as 'under 500'."

@app.route("/")
def home():
    return render_template("index.html", products=PRODUCTS)

@app.route("/recommend", methods=["POST"])
def recommendations():
    data = request.get_json() or {}
    query = data.get("query", "")
    return jsonify({"reply": assistant_reply(query), "products": recommend(query)})

if __name__ == "__main__":
    app.run(debug=True)
