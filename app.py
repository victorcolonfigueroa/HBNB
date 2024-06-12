from api import app, amenities, places, user_routes, country_city_routes
from flask import Flask

app = Flask(__name__)

app.register_blueprint(user_routes)
if __name__ == '__main__':
    app.run(debug=True)
