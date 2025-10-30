import pytest
from application.app import app

# Testar väder-API med en giltig stad
def test_weather_valid_city():
    test_app = app.test_client() # Test_client simulerar en webläsare
    response = test_app.post("/api/weather", data={"cityname": "Stockholm"})
    assert response.status_code == 200
    assert b"Temperature" in response.data or b"Temperatur" in response.data

# Testar väder-API med en ogiltig stad
def test_weather_invalid_city():
    test_app = app.test_client()
    response = test_app.post("/api/weather", data={"cityname": "FakeCity123"})
    assert response.status_code == 200
    assert "Något gick fel" in response.data.decode("utf-8")

# Testar recept-API med en giltig måltid
def test_recipe_valid_meal():
    test_app = app.test_client()
    response = test_app.post("/api/recipe", data={"mealname": "Arrabiata"})
    assert response.status_code == 200
    assert b"Visa recept" in response.data

# Testar recept-API med en ogiltig måltid
def test_recipe_invalid_meal():
    test_app = app.test_client()
    response = test_app.post("/api/recipe", data={"mealname": "xyzxyzxyz"})
    assert response.status_code == 200
    assert b"Inget recept hittades" in response.data