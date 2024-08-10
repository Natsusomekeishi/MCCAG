# -*- coding: utf-8 -*-
from flask import Flask, request, send_file, render_template, jsonify
import os
from image_processing import generate_image_from_skin_file, generate_image
from uuid_fetch import clean_old_cache_files

app = Flask(__name__)
CACHE_DIR = 'static/cache'
CACHE_DURATION = 1  # 1 分钟的秒数

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


@app.before_request
def before_request():
    clean_old_cache_files(CACHE_DIR, CACHE_DURATION)


@app.route('/', methods=['GET', 'POST'])
def index():
    image_url = None
    if request.method == 'POST':
        input_type = request.form.get('input_type')
        avatar_type = request.form.get('avatar_type')

        if input_type == 'username':
            username = request.form.get('username')
            if not username:
                return "玩家名称不能为空", 400
            cache_filename, image_url = generate_image(username, avatar_type)
        elif input_type == 'upload':
            skin_file = request.files.get('skin')
            if not skin_file:
                return "皮肤文件不能为空", 400
            cache_filename, image_url = generate_image_from_skin_file(skin_file, avatar_type)

        if cache_filename is None:
            return "无法生成玩家图像", 500

    return render_template('index.html', image_url=image_url)


@app.route('/mc-avatar-api/head/<username>', methods=['GET'])
def mc_avatar_api_head(username):
    cache_filename, _ = generate_image(username, 'head')
    if cache_filename:
        return send_file(cache_filename)
    return jsonify({"error": "无法生成玩家图像"}), 500


@app.route('/mc-avatar-api/full/<username>', methods=['GET'])
def mc_avatar_api_full(username):
    cache_filename, _ = generate_image(username, 'full')
    if cache_filename:
        return send_file(cache_filename)
    return jsonify({"error": "无法生成玩家图像"}), 500


@app.route('/mc-avatar-api/upload', methods=['POST'])
def mc_avatar_api_upload():
    skin_file = request.files.get('skin')
    avatar_type = request.form.get('avatar_type')

    if not skin_file:
        return jsonify({"error": "皮肤文件不能为空"}), 400

    cache_filename, _ = generate_image_from_skin_file(skin_file, avatar_type)
    if cache_filename:
        return send_file(cache_filename)
    return jsonify({"error": "无法生成玩家图像"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
