from flask import Flask
app = Flask(__name__)

import saleapp.routes

if __name__ == '__main__':
    app.run(debug=True)