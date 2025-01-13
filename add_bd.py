from PIL import Image,ImageDraw,ImageFont,ImageOps
import  os,glob
tgt='./imgdone'
tgt_size=2400
ratio=0.9
border_size=int(0.03*tgt_size)
border_color='black'
exterior=int(0.05*tgt_size)
infor_area=int(0.15*tgt_size)

def process_one_image(img_path):

    img = Image.open(img_path)


    # 计算要将原始图片粘贴到白色背景图上的位置,rotate or not
    rota=True if img.width < img.height * 0.95 else False

    if rota:
        img=img.rotate(90)

    # 计算新的图像尺寸
    new_width = tgt_size
    new_height = int(img.height * new_width / img.width)
    # 重新缩放原始图片
    img = img.resize((new_width, new_height))
    # left = int((tgt_size * (1 - ratio)) // 2)

    # calculate bg size
    background = Image.new('RGB', (tgt_size+2*border_size+2*exterior, new_height+2*border_size+3*exterior+infor_area), (255, 255, 255))
    # add border 1
    img= ImageOps.expand(img, border=border_size, fill=border_color)

    # 将原始图片粘贴到白色背景图上
    background.paste(img, (exterior, exterior))


    # add logo
    logo_img = Image.open('logos/Olympus.png')
    logo_height = infor_area * 0.8
    logo_im=logo_img.resize((int(logo_img.width*logo_height/logo_img.height),int(logo_height)))
    background.paste(logo_img,())
    draw = ImageDraw.Draw(background)
    # add text
    font = ImageFont.truetype("arial.ttf", 80)
    text = "Olympus OM-30 Type.1985\n\nOM-System Zuiko.S 50mm F1,4"
    x, y = exterior, 2 * exterior + new_height + 2*border_size
    draw.text((x, y), text, fill=(0, 0, 0), font=font)
    text2 = "\nShot in Somewhere on the earth."






    if rota:
        img=img.rotate(270)
    # 保存最终结果
    return background.save(os.path.join(tgt, os.path.splitext(os.path.split(img_path)[1])[0] + f".webp"))


if not os.path.exists(tgt):
    os.mkdir(tgt)

# 加载原始图片
img_all=[]
for suf in ['png','jpeg','jpg','PNG']:
    img_all.extend(glob.glob(os.path.join('./imgtoprocess',"*."+suf)))

print(f'Images need to be processed: {img_all}')
for indx in range(len(img_all)):
    print("\rProcessing line {}/{}...".format(indx+1, len(img_all)), end='', flush=True)
    process_res = process_one_image(img_all[indx])
