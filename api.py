from flask import Flask
from flask import jsonify
from flask_cors import CORS, cross_origin
from stock import Stock

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

@app.route("/stocks/<string:stock_name>/", methods=["GET"])
@cross_origin()
def stock_data(stock_name):
    try:
        stock = Stock(stock_name)
        market_cap = stock.get_market_cap()
        covariance, variance, beta = stock.get_beta()
        debt_to_equity_ratio = stock.get_debt_to_equity()
        interest_coverage_ratio = stock.get_interest_coverage()
        return jsonify({"market_cap": market_cap, "covariance": covariance, "variance": variance, "beta": beta,
                        "debt_to_equity_ratio": debt_to_equity_ratio, "interest_coverage_ratio": interest_coverage_ratio})
    except:
        return {jsonify({"error": "Ticker Not Found", "code": "404"})}