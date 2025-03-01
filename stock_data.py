from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/get_stock_info', methods=['GET'])
def get_stock_info():
    code = request.args.get('code')
    if not code:
        return jsonify({"error": "No stock code provided"}), 400

    try:
        stock = yf.Ticker(f"{code}.T")  # 日本株は".T"をつける
        info = stock.info

        data = {
            "code": code,
            "name": info.get("longName", "N/A"),  # 会社名
            "price": info.get("previousClose", "N/A"),  # 株価
            "industry": info.get("industry", "N/A"),  # 業種
            "pastDividend": info.get("trailingAnnualDividendRate", "N/A"),  # 過去配当金
            "forecastDividend": info.get("dividendRate", "N/A")  # 予想配当金
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)