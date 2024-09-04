from PIL import Image,ImageDraw,ImageFont
import  os,glob
tgt='./imgdone'
tgt_size=2400
ratio=0.9

if not os.path.exists(tgt):
    os.mkdir(tgt)

# 加载原始图片
img_all=[]
for suf in ['png','jpeg','jpg','PNG']:
    img_all.extend(glob.glob(os.path.join('./imgtoprocess',"*."+suf)))

print(f'Images need to be processed: {img_all}')
for indx in range(len(img_all)):
    print("\rProcessing line {}/{}...".format(indx+1, len(img_all)), end='', flush=True)
    img_path=img_all[indx]
    img = Image.open(img_path)
    background = Image.new('RGB', (tgt_size, tgt_size), (255, 255, 255))

    # 计算要将原始图片粘贴到白色背景图上的位置
    if img.width>img.height*0.95:
        # 计算新的图像尺寸
        new_width = int(tgt_size*ratio)
        new_height = int(img.height * new_width / img.width)
        # 重新缩放原始图片
        img = img.resize((new_width, new_height))
        left = int((tgt_size *(1-ratio)) // 2)
        top = 100
        # 将原始图片粘贴到白色背景图上
        background.paste(img, (left, top))
        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype("arial.ttf", 100)
        text = "Olympus OM-30 Type.1985\nOM-System Zuiko.S 50mm F1,4\nShot in Somewhere on the earth."
        x, y = left, 2*top+new_height
        draw.text((x, y), text, fill=(0, 0, 0), font=font)
    else:
        new_height = int(tgt_size*ratio)
        new_width = int(img.width * new_height / img.height)
        # 重新缩放原始图片
        img = img.resize((new_width, new_height))
        top = int((tgt_size *(1-ratio)) // 2)
        left = 100
        # 将原始图片粘贴到白色背景图上
        background.paste(img, (left, top))
        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype("arial.ttf", 100)
        text = "Olympus OM-30 Type.1985\nOM-System Zuiko.S 50mm F1,4\nShot in Somewhere on the earth."
        x, y = 100, 50
        draw.text((x, y), text, fill=(0, 0, 0), font=font)

    # 保存最终结果
    background.save(os.path.join(tgt, os.path.splitext(os.path.split(img_path)[1])[0]+f".webp"))