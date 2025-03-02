from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/get_stock_info', methods=['GET'])
def get_stock_info():
    code = request.args.get('code')
    if not code:
        return jsonify({"error": "No stock code provided"}), 400

    try:
        # 日本株は".T"をつける
        stock = yf.Ticker(f"{code}.T")

        # 最後の1分の株価を取得
        data = stock.history(period="1d", interval="1m")  # 1分ごとのデータ
        if not data.empty:
            latest_data = data.iloc[-1]  # 最新の株価
            price = latest_data['Close']
        else:
            price = 'N/A'

        # その他の情報を取得
        info = stock.info
        name = info.get("longName", "N/A")  # 会社名
        industry = info.get("industry", "N/A")  # 業種
        past_dividend = info.get("trailingAnnualDividendRate", "N/A")  # 過去配当金
        forecast_dividend = info.get("dividendRate", "N/A")  # 予想配当金

        # 結果を返す
        data = {
            "code": code,
            "name": name,
            "price": price,
            "industry": industry,
            "pastDividend": past_dividend,
            "forecastDividend": forecast_dividend
        }
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
