from PIL import Image, ImageDraw

# 创建256x256的图像
img = Image.new('RGB', (256, 256), (52, 152, 219))
draw = ImageDraw.Draw(img)

# 绘制文件夹
draw.rectangle([50, 80, 200, 180], fill=(41, 128, 185))
draw.rectangle([50, 60, 110, 85], fill=(41, 128, 185))

# 保存为ICO
img.save('app_icon.ico')
print("图标已创建")
