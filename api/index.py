#!/usr/bin/env python3
"""
栖养生活健康顾问系统 - Vercel API入口
"""

from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.json')

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f)

def load_users():
    ensure_data_dir()
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_users(users):
    ensure_data_dir()
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'service': '栖养生活健康顾问', 'timestamp': datetime.now().isoformat()})

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': '请提供JSON数据'}), 400
        user_id = data.get('user_id', 'anonymous')
        message = data.get('message', '')
        if not message:
            return jsonify({'success': False, 'error': '消息不能为空'}), 400
        response = {
            'success': True,
            'user_id': user_id,
            'reply': f'收到：「{message}」\n\n我是栖养生活健康顾问，正在为您分析...',
            'timestamp': datetime.now().isoformat()
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/user/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': '请提供JSON数据'}), 400
        user_id = data.get('user_id')
        nickname = data.get('nickname', '未命名用户')
        if not user_id:
            return jsonify({'success': False, 'error': 'user_id不能为空'}), 400
        users = load_users()
        if user_id in users:
            return jsonify({'success': False, 'error': '用户已存在'}), 409
        users[user_id] = {'nickname': nickname, 'created_at': datetime.now().isoformat()}
        save_users(users)
        return jsonify({'success': True, 'user_id': user_id, 'nickname': nickname})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

handler = app
