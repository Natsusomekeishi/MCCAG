# -*- coding: utf-8 -*-
from flask import Flask, request, send_file, render_template, url_for, jsonify
import requests
import base64
import json
from PIL import Image, ImageFilter, ImageOps
from io import BytesIO
import os
import time

app = Flask(__name__)
CACHE_DIR = 'static/cache'
CACHE_DURATION = 10 * 60  # 10 分钟的秒数

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def get_uuid_by_name(username):
    """根据玩家名称获取 UUID。"""
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    response = requests.get(url)
    
    if response.status_code == 404:
        return None
    
    data = response.json()
    return data['id']

def get_player_textures(uuid):
    """根据 UUID 获取玩家的皮肤纹理信息。"""
    url = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}?unsigned=false"
    response = requests.get(url)
    
    if response.status_code != 200:
        return None
    
    data = response.json()
    
    if 'properties' not in data:
        return None
    
    properties = data['properties']
    
    for prop in properties:
        if prop['name'] == 'textures':
            textures_base64 = prop['value']
            textures_json = base64.b64decode(textures_base64).decode('utf-8')
            textures = json.loads(textures_json)
            return textures
    
    return None

def download_image(url):
    """下载图像并返回 PIL 图像对象。"""
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        return None

def create_image_with_paste(source_image, target_image_path, canvas_size, operations):
    """创建图像并保存到目标路径。"""
    canvas = Image.new('RGBA', canvas_size, (255, 255, 255, 0))
    skin_size = source_image.size

    # 根据皮肤尺寸选择缩放
    if skin_size == (64, 32):
        resized_source_image = source_image.resize((128, 64), Image.NEAREST)
    else:
        resized_source_image = source_image.resize((128, 128), Image.NEAREST)

    for operation in operations:
        crop_box, scale_factor, paste_position, *mirror = operation

        cropped_image = resized_source_image.crop(crop_box)
        if mirror:
            cropped_image = ImageOps.mirror(cropped_image)
            
        new_size = (int(cropped_image.size[0] * scale_factor), int(cropped_image.size[1] * scale_factor))
        bordered_size = (new_size[0] + 30, new_size[1] + 30)
        bordered_image = Image.new('RGBA', bordered_size, (0, 0, 0, 0))
        bordered_image.paste(cropped_image.resize(new_size, Image.NEAREST), (15, 15))

        mask = bordered_image.split()[3]
        solid_image = Image.new('RGBA', bordered_image.size, (75, 85, 142, 255))
        shadow_image = Image.composite(solid_image, Image.new('RGBA', bordered_image.size), mask)
        blurred_shadow = shadow_image.filter(ImageFilter.GaussianBlur(7))
        alpha = blurred_shadow.split()[3].point(lambda p: p * 0.5)
        blurred_shadow.putalpha(alpha)

        shadow_position = (paste_position[0] - 15, paste_position[1] - 10)
        canvas.paste(blurred_shadow, shadow_position, blurred_shadow)

        adjusted_paste_position = (paste_position[0] - 15, paste_position[1] - 15)
        canvas.paste(bordered_image, adjusted_paste_position, bordered_image)

    canvas.save(target_image_path)

def get_cache_filename(username):
    """根据用户名生成缓存文件名。"""
    uuid = get_uuid_by_name(username)
    return os.path.join(CACHE_DIR, f'{uuid}.png') if uuid else None

def is_cache_valid(filename):
    """检查缓存是否有效。"""
    ignore_filename = '923ed5ce249a4cd3ac7d23e6797b939c.png'
    
    if os.path.basename(filename) == ignore_filename:
        return True

    if os.path.exists(filename):
        return time.time() - os.path.getmtime(filename) < CACHE_DURATION
    return False

@app.route('/', methods=['GET', 'POST'])
def index():
    image_url = None
    if request.method == 'POST':
        username = request.form.get('username')
        if not username:
            return "玩家名称不能为空", 400

        cache_filename = get_cache_filename(username)

        if cache_filename and is_cache_valid(cache_filename):
            image_url = url_for('static', filename=f'cache/{os.path.basename(cache_filename)}')
        else:
            uuid = get_uuid_by_name(username)
            if uuid is None:
                return "没有找到该玩家", 404

            textures = get_player_textures(uuid)
            if textures is None:
                return "无法获取玩家纹理信息", 500

            if 'SKIN' in textures['textures']:
                skin_url = textures['textures']['SKIN']['url']
                skin_image = download_image(skin_url)
                
                if skin_image:
                    target_image_path = cache_filename
                    canvas_size = (1000, 1000)  # 新画布的大小
                    skin_size = skin_image.size

                    if skin_size == (64, 32):
                        operations = [
                            ((8, 40, 16, 64), 8.375, (434,751)), # 右腿
                            ((8, 40, 16, 64), 8.375, (505,751), True), # 左腿，使用右腿镜像
                            ((86, 40, 92, 64), 8.167, (388,561)), # 右臂
                            ((86, 40, 92, 64), 8.167, (566,561), True), # 左臂，使用右臂镜像
                            ((40, 40, 56, 64), 8.0625, (437,561)), # 躯干
                            ((16, 16, 32, 32), 26.875, (287,131)), # 头部
                            ((80, 16, 96, 32), 30.8125, (254,107)), # 头部外层
                        ]
                    else:
                        operations = [
                            ((8, 40, 16, 64), 8.375, (434,751)),
                            ((8, 72, 16, 96), 9.375, (428,737)),
                            ((40, 104, 48, 128), 8.375, (505,751)),
                            ((8, 104, 16, 128), 9.375, (503,737)),
                            ((86, 40, 92, 64), 8.167, (388,561)),
                            ((88, 72, 94, 96), 9.5, (382,538)),
                            ((74, 104, 80, 128), 8.167, (566,561)),
                            ((104, 104, 110, 128), 9.5, (564,538)),
                            ((40, 40, 56, 64), 8.0625, (437,561)),
                            ((40, 72, 56, 96), 8.6575, (432,555)),
                            ((16, 16, 32, 32), 26.875, (287,131)),
                            ((80, 16, 96, 32), 30.8125, (254,107)),
                        ]

                    create_image_with_paste(skin_image, target_image_path, canvas_size, operations)
                    image_url = url_for('static', filename=f'cache/{os.path.basename(target_image_path)}')
    
    return render_template('index.html', image_url=image_url)

@app.route('/mc-avatar-api/<username>', methods=['GET'])
def mc_avatar_api(username):
    cache_filename = get_cache_filename(username)

    if cache_filename and is_cache_valid(cache_filename):
        return send_file(cache_filename)
    
    uuid = get_uuid_by_name(username)
    if uuid is None:
        return jsonify({"error": "没有找到该玩家"}), 404

    textures = get_player_textures(uuid)
    if textures is None:
        return jsonify({"error": "无法获取玩家纹理信息"}), 500

    if 'SKIN' in textures['textures']:
        skin_url = textures['textures']['SKIN']['url']
        skin_image = download_image(skin_url)
        
        if skin_image:
            target_image_path = cache_filename
            canvas_size = (1000, 1000)  # 新画布的大小
            skin_size = skin_image.size

            if skin_size == (64, 32):
                operations = [
                    ((8, 40, 16, 64), 8.375, (434,751)), # 右腿
                    ((8, 40, 16, 64), 8.375, (505,751), True), # 左腿，使用右腿镜像
                    ((86, 40, 92, 64), 8.167, (388,561)), # 右臂
                    ((86, 40, 92, 64), 8.167, (566,561), True), # 左臂，使用右臂镜像
                    ((40, 40, 56, 64), 8.0625, (437,561)), # 躯干
                    ((16, 16, 32, 32), 26.875, (287,131)), # 头部
                    ((80, 16, 96, 32), 30.8125, (254,107)), # 头部外层
                ]
            else:
                operations = [
                    ((8, 40, 16, 64), 8.375, (434,751)),
                    ((8, 72, 16, 96), 9.375, (428,737)),
                    ((40, 104, 48, 128), 8.375, (505,751)),
                    ((8, 104, 16, 128), 9.375, (503,737)),
                    ((86, 40, 92, 64), 8.167, (388,561)),
                    ((88, 72, 94, 96), 9.5, (382,538)),
                    ((74, 104, 80, 128), 8.167, (566,561)),
                    ((104, 104, 110, 128), 9.5, (564,538)),
                    ((40, 40, 56, 64), 8.0625, (437,561)),
                    ((40, 72, 56, 96), 8.6575, (432,555)),
                    ((16, 16, 32, 32), 26.875, (287,131)),
                    ((80, 16, 96, 32), 30.8125, (254,107)),
                ]

            create_image_with_paste(skin_image, target_image_path, canvas_size, operations)
            return send_file(target_image_path)

    return jsonify({"error": "没有找到皮肤信息"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
