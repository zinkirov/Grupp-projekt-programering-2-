from flask import Flask, render_template, request, make_response
import requests
import json
import pandas as pd
import plotly.express as px
import random
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/form")
def form():
    last_city = request.cookies.get("last_city", "")
    return render_template("form.html", last_city=last_city)

@app.route("/form2")
def form2():
    last_meal = request.cookies.get("last_meal", "")
    return render_template("form2.html", last_meal=last_meal)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/api/weather", methods=["POST"])
def api_weather():
    try:
        city_name = request.form["cityname"]
        data_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=95fccd7b6adddb581a8319f61f3b71ff&units=metric"
        json_data = requests.get(data_url)

        data = json.loads(json_data.text)
        # Extrahera relevanta fält
        weather_info = {
            "City": data["name"],
            "Temperature (°C)": data["main"]["temp"],
            "Condition": data["weather"][0]["main"],
            "Description": data["weather"][0]["description"]
        }
        # Skapa DataFrame
        df = pd.DataFrame([weather_info])
        table_data = df.to_html(
            columns=["City", "Temperature (°C)", "Condition", "Description"],
            classes="table p-5",
            justify="left"
        )
        resp = make_response(render_template("form.html", data=table_data))
        resp.set_cookie("last_city", city_name)
        return resp

    except Exception as e:
        return f"Något gick fel med väderhämtningen: {e}"

@app.route("/api/recipe", methods=["POST"])
def api_recipe():
    """Funktionen """
    try:
        meal_name = request.form["mealname"]
        data_url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={meal_name}"
        response = requests.get(data_url)
        data = response.json()

        meals = data.get("meals")
        if not meals:
            return render_template("form2.html", data="<p>Inget recept hittades.</p>")

        # Skapar ny lista med omdöpta kolumner
        recipe_info = []
        for meal in meals:
            recipe_info.append({
                "Namn": meal["strMeal"],
                "Kategori": meal["strCategory"],
                "Instruktioner":f'<a href="https://www.themealdb.com/meal/{meal["idMeal"]}" target="_blank">Visa recept</a>',
                "Bild": f'<img src="{meal["strMealThumb"]}" width="100">',
                "Video": f'<a href="{meal["strYoutube"]}" target="_blank">Se video</a>'
            })

        df = pd.DataFrame(recipe_info)

        table_data = df.to_html(
            escape=False,
            columns=["Namn", "Kategori", "Instruktioner", "Bild", "Video"],
            classes="table p-5",
            justify="left"
        )

        resp = make_response(render_template("form2.html", data=table_data))
        resp.set_cookie("last_meal", meal_name)
        return resp

    except Exception as e:
        return f"Något gick fel med recepthämtningen: {e}"
    
@app.route("/api/combo", methods=["POST"])
def api_combo():
    try:
        # Hämtar stad från formuläret
        city_name = request.form["cityname"]
         # Hämtar väderdata från OpenWeatherMap
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=95fccd7b6adddb581a8319f61f3b71ff&units=metric"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        
        condition = weather_data["weather"][0]["main"]
        temperature = weather_data["main"]["temp"]
        
        if condition.lower() in ["rain", "drizzle", "thunderstorm"]:
            tag = "Starter"
        elif 1<= temperature <= 10:
            tag = "Pasta"
        elif 10 < temperature < 15:
            tag = "Vegetarian"
        elif 15 <= temperature <= 25:
            tag = random.choice(["Beef", "Chicken", "Seafood","Lamb"])
        else:
            tag = random.choice([
    "Beef",
    "Breakfast",
    "Chicken",
    "Dessert",
    "Lamb",
    "Pasta",
    "Pork",
    "Seafood",
    "Starter",
    "Vegan",
    "Vegetarian"
])
        # Hämtar recept från TheMealDB baserat på tagg
        recipe_url = f"https://www.themealdb.com/api/json/v1/1/filter.php?c={tag}"
        recipe_response = requests.get(recipe_url)
        recipe_data = recipe_response.json()

        meals = recipe_data.get("meals", [])
        if not meals:
            return render_template("form.html", data="<h2>Inga recept hittades för vädret.</h2>")
        # Skapar tabell med receptnamn, bild och länk
        recipe_info = []
        for meal in meals:
            recipe_info.append({
                "Meal": meal["strMeal"],
                "Image": f'<img src="{meal["strMealThumb"]}" width="100">',
                "Details": f'<a href="https://www.themealdb.com/meal/{meal["idMeal"]}" target="_blank">Visa recept</a>'
            })
        df = pd.DataFrame(recipe_info)
        table_data = df.to_html(escape=False, classes="table p-5", justify="left")
        resp = make_response(render_template("post_form.html", data=table_data))
        resp.set_cookie("last_city", city_name)
        resp.set_cookie("last_category", tag)
        return resp
    except Exception as e:
        return f"Något gick fel i kombinerad hämtning: {e}"
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    

if __name__ == "__main__":
    app.run()



