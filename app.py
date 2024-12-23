from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # 启用跨域资源共享

# MongoDB 设置
client = MongoClient('mongodb://localhost:27017/')
db = client['gobang']
players_collection = db['players']

@app.route('/register', methods=['POST'])
def register_player():
    username = request.json.get('username')
    if not username:
        return jsonify({'error': '用户名不能为空'}), 400

    existing_player = players_collection.find_one({'username': username})
    if existing_player:
        return jsonify({'error': '玩家已存在'}), 400

    player = {'username': username, 'scores': []}
    players_collection.insert_one(player)
    return jsonify(player), 201

@app.route('/score', methods=['POST'])
def submit_score():
    username = request.json.get('username')
    score = request.json.get('score')

    if not username or score is None:
        return jsonify({'error': '用户名和分数不能为空'}), 400

    player = players_collection.find_one({'username': username})
    if not player:
        return jsonify({'error': '玩家不存在'}), 404

    players_collection.update_one({'username': username}, {'$push': {'scores': score}})
    player['scores'].append(score)  # 更新返回的玩家信息
    return jsonify(player), 200

@app.route('/player/<username>', methods=['GET'])
def get_player_info(username):
    player = players_collection.find_one({'username': username})
    if not player:
        return jsonify({'error': '玩家不存在'}), 404

    return jsonify(player), 200

if __name__ == '__main__':
    app.run(debug=True)
