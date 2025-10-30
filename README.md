
En Flask-baserad webapp som kombinerar väderdata med receptförslag. Användaren kan söka efter väder i en stad, recept på en måltid, eller få automatiska recept baserat på väderförhållanden.

# Funktioner

- Sök väder via OpenWeatherMap API
- Sök recept via TheMealDB API
- Kombinera väder + recept (t.ex. pasta vid kallt väder)
- Cookies för att spara senaste sökning
- Bootstrap-tabeller för snygg presentation
- Felhantering med 404-sida

# Map struktur
application/
├── app.py
├── templates/
│   ├── main.html
│   ├── form.html
│   ├── form2.html
│   ├── post_form.html
│   └── 404.html
├── static/
│   └── style.css
tests/
├── test_api.py