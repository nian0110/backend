# app.py
from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # 允許所有來源的 CORS

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/images", methods=["POST"])
def get_images():
    # 讀取CSV文件
    df = pd.read_csv("images.csv")
    
    # 從請求的 JSON 內容中獲取 limit 參數
    data = request.get_json()
    limit = int(data.get('limit', 10))  # 預設為10
    
    # 創建包含filename和full_path的列表
    images = [
        {
            "filename": filename,
            "full_path": f"./images/{filename}"
        }
        for filename in df['filename']
    ]
    
    # 隨機選取 N 張圖片
    random.shuffle(images)  # 打亂圖片列表
    selected_images = images[:limit]  # 選取指定數量的圖片

    # 返回 JSON 格式
    result = {
        "totalImagesCount": df.shape[0],
        "Images": selected_images
    }
    
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)