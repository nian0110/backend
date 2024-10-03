from flask import Flask, jsonify, request, render_template, url_for
import pandas as pd
from flask_cors import CORS
import random
import os

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/index')
def index2():
    return render_template('index.html')

@app.route("/get_data", methods=["POST"])
def get_data():
    data = request.get_json()
    A_list = ['活動']
    B_list = data.get('B', [])
    limit = int(data.get('limit', 10))
    app.logger.info(f'A_list: {A_list}')
    app.logger.info(f'B_list: {B_list}')

    # 读取CSV文件
    df = pd.read_csv('images.csv')

    # 根据A_list和B_list过滤数据
    df_result = df[df['root_path'].isin(A_list)]
    df_result = df_result[df_result['lingorm'].isin(B_list)]
    app.logger.info(f'df_result: {df_result.shape}')

    # 創建包含filename和full_path的列表
    images = [
        {
            "filename": filename,
            "full_path": url_for('static', filename=f'images/{filename}')  # 使用 url_for 生成正確的 URL
        }
        for filename in df_result['filename']
    ]
    
    # 隨機選取 N 張圖片
    random.shuffle(images)
    selected_images = images[:limit]

    # 返回 JSON 格式
    result = {
        "totalImagesCount": len(images),
        "Images": selected_images
    }
    app.logger.info(f'result: {len(selected_images)}')
    
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)