# -*- coding: utf-8 -*-
from PIL import Image, ImageFilter, ImageOps
import os
import requests
from io import BytesIO

from flask import url_for

from uuid_fetch import get_uuid_by_name, get_player_textures, get_cache_filename, is_cache_valid

CACHE_DIR = 'static/cache'
CACHE_DURATION = 1 * 60  # 1 分钟的秒数


def download_image(url):
    """下载图像并返回 PIL 图像对象。"""
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    return None


def create_image_with_paste(source_image, target_image_path, canvas_size, operations):
    """创建图像并保存到目标路径。"""
    canvas = Image.new('RGBA', canvas_size, (255, 255, 255, 0))
    skin_size = source_image.size

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
        shadow_image = Image.new('RGBA', bordered_image.size, (0, 0, 0, 0))
        shadow_image.paste(solid_image, (0, 0), mask)
        blurred_shadow = shadow_image.filter(ImageFilter.GaussianBlur(7))
        alpha = blurred_shadow.split()[3].point(lambda p: p * 0.6)
        blurred_shadow.putalpha(alpha)

        shadow_position = (paste_position[0] - 15, paste_position[1] - 10)
        base_image = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
        base_image.paste(blurred_shadow, shadow_position, blurred_shadow)
        canvas = Image.alpha_composite(canvas, base_image)

        adjusted_paste_position = (paste_position[0] - 15, paste_position[1] - 15)
        canvas.paste(bordered_image, adjusted_paste_position, bordered_image)

    canvas.save(target_image_path)


def generate_image(username, avatar_type):
    cache_filename = get_cache_filename(username)
    if cache_filename and is_cache_valid(cache_filename, CACHE_DURATION):
        return cache_filename, url_for('static', filename=f'cache/{os.path.basename(cache_filename)}')

    uuid = get_uuid_by_name(username)
    if uuid is None:
        return None, None

    textures = get_player_textures(uuid)
    if textures is None or 'SKIN' not in textures['textures']:
        return None, None

    skin_url = textures['textures']['SKIN']['url']
    skin_image = download_image(skin_url)

    if skin_image:
        canvas_size = (1000, 1000)

        if avatar_type == 'head':
            operations = [
                ((16, 16, 32, 32), 42, (165, 155)),
                ((80, 16, 96, 32), 45, (140, 135)),
            ]
        else:
            operations = [
                ((8, 40, 16, 64), 8.375, (434, 751)),
                ((8, 72, 16, 96), 9.375, (428, 737)),
                ((40, 104, 48, 128), 8.375, (505, 751)),
                ((8, 104, 16, 128), 9.375, (503, 737)),
                ((86, 40, 92, 64), 8.167, (388, 561)),
                ((88, 72, 94, 96), 9.5, (382, 538)),
                ((74, 104, 80, 128), 8.167, (566, 561)),
                ((104, 104, 110, 128), 9.5, (564, 538)),
                ((40, 40, 56, 64), 8.0625, (437, 561)),
                ((40, 72, 56, 96), 8.6575, (432, 555)),
                ((16, 16, 32, 32), 26.875, (287, 131)),
                ((80, 16, 96, 32), 30.8125, (254, 107)),
            ]

        create_image_with_paste(skin_image, cache_filename, canvas_size, operations)
        return cache_filename, url_for('static', filename=f'cache/{os.path.basename(cache_filename)}')

    return None, None


def generate_image_from_skin_file(skin_file, avatar_type):
    cache_filename = os.path.join(CACHE_DIR, f'{skin_file.filename}.png')

    if is_cache_valid(cache_filename, CACHE_DURATION):
        return cache_filename, url_for('static', filename=f'cache/{os.path.basename(cache_filename)}')

    skin_image = Image.open(skin_file)

    if skin_image:
        canvas_size = (1000, 1000)

        if avatar_type == 'head':
            operations = [
                ((16, 16, 32, 32), 42, (165, 155)),
                ((80, 16, 96, 32), 45, (140, 135)),
            ]
        else:
            operations = [
                ((8, 40, 16, 64), 8.375, (434, 751)),
                ((8, 72, 16, 96), 9.375, (428, 737)),
                ((40, 104, 48, 128), 8.375, (505, 751)),
                ((8, 104, 16, 128), 9.375, (503, 737)),
                ((86, 40, 92, 64), 8.167, (388, 561)),
                ((88, 72, 94, 96), 9.5, (382, 538)),
                ((74, 104, 80, 128), 8.167, (566, 561)),
                ((104, 104, 110, 128), 9.5, (564, 538)),
                ((40, 40, 56, 64), 8.0625, (437, 561)),
                ((40, 72, 56, 96), 8.6575, (432, 555)),
                ((16, 16, 32, 32), 26.875, (287, 131)),
                ((80, 16, 96, 32), 30.8125, (254, 107)),
            ]

        create_image_with_paste(skin_image, cache_filename, canvas_size, operations)
        return cache_filename, url_for('static', filename=f'cache/{os.path.basename(cache_filename)}')

    return None, None
