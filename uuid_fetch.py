# -*- coding: utf-8 -*-
# 负责获取玩家皮肤
import base64

import requests
import os
import time

from flask import json

CACHE_DIR = 'static/cache'


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


def get_cache_filename(username):
    """根据用户名生成缓存文件名。"""
    uuid = get_uuid_by_name(username)
    return os.path.join(CACHE_DIR, f'{uuid}.png') if uuid else None


def is_cache_valid(fileName, cache_duration):
    """检查缓存是否有效。"""
    ignore_filename = '923ed5ce249a4cd3ac7d23e6797b939c.png'

    if os.path.basename(fileName) == ignore_filename:
        return True

    if os.path.exists(fileName):
        return time.time() - os.path.getmtime(fileName) < cache_duration
    return False


def clean_old_cache_files(cache_dir, cache_duration):
    """删除超过指定时间的缓存文件，但保留特定的忽略文件。"""
    ignore_filename = '923ed5ce249a4cd3ac7d23e6797b939c.png'
    now = time.time()
    for filename in os.listdir(cache_dir):
        if filename == ignore_filename:
            continue
        filepath = os.path.join(cache_dir, filename)
        if os.path.isfile(filepath) and now - os.path.getmtime(filepath) > cache_duration:
            os.remove(filepath)
