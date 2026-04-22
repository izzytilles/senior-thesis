import json
import os
from datetime import datetime
from flask import Flask, request, redirect, url_for, session, render_template
from openai import AzureOpenAI
from dotenv import load_dotenv
 
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

SEASONAL_DATA = None

def load_seasonal_produce():
    """
    Loads and parses seasonal.json at startup
    """
    global SEASONAL_DATA
    if SEASONAL_DATA is None:
        with open(os.path.join(os.path.dirname(__file__), "data", "seasonal.json"), "r") as f:
            SEASONAL_DATA = json.load(f)
    return SEASONAL_DATA

def get_seasonal_produce(location, month):
    """
    Takes info about user's location and current month, queries seasonal.json, returns list of in-season produce 
    """
    data = load_seasonal_produce()
    location_data = data.get(location, {})
    return location_data.get(month, [])


def generate_recipes(produce_list):
    """
    Constructs prompt, calls AI API (OpenAI via Azure for now), returns list of recipes
    """
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )

    produce_str = ", ".join(produce_list)

    prompt = (
        f"Generate 3 seasonal recipes using the following in-season produce: {produce_str}. "
        "Each recipe should include at least one of the listed items as a star ingredient."
        "All selected produce should be featured in at least one recipe."
        "For each recipe, provide: a title, a short description (1-2 sentences), "
        "a list of ingredients, and step-by-step instructions. "
        "Prioritize simple, whole-ingredient cooking that highlights the produce itself. "
        "Format each recipe clearly with headers."
    )

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        messages=[
            {"role": "user", "content": (
                "You are a seasonal cooking assistant. You generate recipes that celebrate "
                "fresh, local, in-season produce. Your recipes are practical, ingredient-forward, "
                "and accessible to home cooks.\n\n" + prompt
            )},
        ],
        max_completion_tokens=8000,
    )

    return response.choices[0].message.content

def get_current_month():
    """
    Returns current month as a string
    """
    return str(datetime.now().month).zfill(2)



@app.route("/", methods=["GET"])
def index():
    """Serve the location selection page."""
    data = load_seasonal_produce()
    locations = list(data.keys())
    return render_template("location.html", locations=locations)


@app.route("/produce", methods=["POST"])
def produce():
    """Receive selected location, return produce selection page with in-season items."""
    location = request.form.get("location")
    if not location:
        return redirect(url_for("index"))

    month = get_current_month()
    seasonal_items = get_seasonal_produce(location, month)

    session["location"] = location
    session["month"] = month

    return render_template("produce.html", produce=seasonal_items, location=location)


@app.route("/recipes", methods=["POST"])
def recipes():
    """Receive selected produce items, return recipes page with AI-generated content."""
    selected = request.form.getlist("produce")
    if not selected:
        location = session.get("location")
        month = session.get("month")
        seasonal_items = get_seasonal_produce(location, month) if location else []
        return render_template(
            "produce.html",
            produce=seasonal_items,
            location=location,
            error="Select at least one item.",
        )

    try:
        recipe_content = generate_recipes(selected)
    except Exception as e:
        recipe_content = f"Error generating recipes: {e}"
    return render_template("recipes.html", recipes=recipe_content, selected=selected)

if __name__ == "__main__":
    app.run(debug=True)