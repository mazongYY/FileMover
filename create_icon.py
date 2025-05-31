#!/usr/bin/env python3
"""
创建应用图标的脚本
生成一个简单的文件夹图标作为应用图标
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_app_icon():
    """创建应用图标"""
    # 创建256x256的图像
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 绘制文件夹背景
    folder_color = (52, 152, 219)  # 蓝色
    folder_width = int(size * 0.8)
    folder_height = int(size * 0.6)
    folder_x = (size - folder_width) // 2
    folder_y = (size - folder_height) // 2 + 20

    # 绘制文件夹主体
    draw.rectangle(
        [folder_x, folder_y, folder_x + folder_width, folder_y + folder_height],
        fill=folder_color,
        outline=(41, 128, 185)
    )

    # 绘制文件夹标签
    tab_width = folder_width // 3
    tab_height = 20
    draw.rectangle(
        [folder_x, folder_y - tab_height, folder_x + tab_width, folder_y + 5],
        fill=folder_color,
        outline=(41, 128, 185)
    )

    # 绘制搜索图标
    search_center_x = folder_x + folder_width - 40
    search_center_y = folder_y + 30
    search_radius = 15

    # 搜索圆圈
    draw.ellipse(
        [search_center_x - search_radius, search_center_y - search_radius,
         search_center_x + search_radius, search_center_y + search_radius],
        outline=(255, 255, 255),
        width=4
    )

    # 搜索手柄
    handle_start_x = search_center_x + search_radius - 3
    handle_start_y = search_center_y + search_radius - 3
    handle_end_x = handle_start_x + 12
    handle_end_y = handle_start_y + 12
    draw.line(
        [handle_start_x, handle_start_y, handle_end_x, handle_end_y],
        fill=(255, 255, 255),
        width=4
    )

    # 绘制文件图标
    file_x = folder_x + 20
    file_y = folder_y + 40
    file_width = 25
    file_height = 35

    for i in range(3):
        x_offset = i * 30
        draw.rectangle(
            [file_x + x_offset, file_y, file_x + x_offset + file_width, file_y + file_height],
            fill=(255, 255, 255),
            outline=(189, 195, 199)
        )

    # 添加文字（如果可能）
    try:
        # 尝试使用系统字体
        font_size = 24
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # 如果没有找到字体，使用默认字体
        font = ImageFont.load_default()

    text = "筛选"
    try:
        text_width, text_height = draw.textsize(text, font=font)
    except:
        # 如果textsize也不可用，使用估算值
        text_width = len(text) * 12
        text_height = 16
    text_x = (size - text_width) // 2
    text_y = folder_y + folder_height + 10

    # 绘制文字阴影
    draw.text((text_x + 2, text_y + 2), text, font=font, fill=(0, 0, 0, 128))
    # 绘制文字
    draw.text((text_x, text_y), text, font=font, fill=(44, 62, 80))

    # 保存为不同尺寸的ICO文件
    icon_sizes = [16, 32, 48, 64, 128, 256]
    images = []

    for icon_size in icon_sizes:
        resized_img = img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        images.append(resized_img)

    # 保存ICO文件
    images[0].save('app_icon.ico', format='ICO', sizes=[(s, s) for s in icon_sizes])
    print("应用图标已创建: app_icon.ico")

    # 也保存为PNG文件用于预览
    img.save('app_icon.png', format='PNG')
    print("图标预览已创建: app_icon.png")

if __name__ == "__main__":
    try:
        create_app_icon()
    except ImportError:
        print("需要安装Pillow库: pip install Pillow")
    except Exception as e:
        print(f"创建图标时出错: {e}")
