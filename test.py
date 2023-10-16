from flask import Flask, render_template, jsonify
import random
import time

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('test-1.html')


@app.route('/get_location')
def get_location():
    # 仮の位置情報データを生成（ランダムな座標を返す例）
    latitude = 35.8367+ random.uniform(-0.01, 0.01)
    longitude = 139.6603 + random.uniform(-0.01, 0.01)

    return jsonify(latitude=latitude, longitude=longitude)


if __name__ == '__main__':
    app.run(debug=True)
