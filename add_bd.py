from PIL import Image,ImageDraw,ImageFont,ImageOps
import  os,glob
from color_extract import  extract_main_colors
import numpy as np

src='./imgtoprocess'
tgt='./imgdone'
tgt_size=2400
ratio=0.9
border_size=int(0.015*tgt_size)
border_color='black'
exterior=int(0.05*tgt_size)
infor_area=int(0.15*tgt_size)
font_size=int(tgt_size*0.03)

text_dict={
    'hassel_CF60':["Hasselblad 500CM Type.1990s\n\nCarl Zeiss CF 60mm F3,5",'logos/hassel.jpg'],
    'hassel_CF150': ["Hasselblad 500CM Type.1990s\n\nCarl Zeiss CF 150mm F4", 'logos/hassel.jpg'],
    'olym_50': ["Olympus OM-30\n\nG.Zuiko Auto-S 50mm F1,4", 'logos/Olympus.jpg'],
    'olym_135': ["Olympus OM-30\n\nZuiko MC Auto-T 135mm F2,8", 'logos/Olympus.jpg'],
    'olym_2848': ["Olympus OM-30\n\nZuiko S Auto-Zoom 28-48mm F4", 'logos/Olympus.jpg'],
    'mamiya_six': ["Mamiya-Six Type.K-1953\n\nOlympus D.Zuiko F.C. 75mm F3.5 Sekorsha", 'logos/mamiya.jpg'],
    'minolta': ["Minolta Hi-Matic E \n\nRokkor-QF 40mm F1,7", 'logos/Minolta.jpg'],

}
# text = "Olympus OM-30 Type.1985\n\nOM-System Zuiko.S 50mm F1,4"
# text = "Minolta Hi-Matic E Type.1982\n\nRokkor-QF 40mm F1,7"

# logo_path='logos/Olympus.jpg'
# logo_path='logos/Minolta.jpg'
# logo_path='logos/mamiya.jpg'
# logo_path='logos/mamiya2.jpg'

def rotate_image_90_no_crop(image_data,reverse=False):
    # 打开图像
    image=image_data
    width, height = image.size

    # 创建一个新的背景图像，尺寸为原图像的对角线长度
    new_size = int((width ** 2 + height ** 2) ** 0.5)
    new_image = Image.new("RGB", (new_size, new_size), (0, 0,0))

    # 将原图像粘贴到背景图像的中心
    new_image.paste(image, ((new_size - width) // 2, (new_size - height) // 2))

    # 旋转图像90度
    if not reverse:
        rotated_image = new_image.rotate(90, expand=True)
    else:
        rotated_image = new_image.rotate(270, expand=True)

    # 裁剪掉多余的透明部分
    bbox = rotated_image.getbbox()
    cropped_image = rotated_image.crop(bbox)

    return cropped_image

def process_one_image(img_path,text,logo_file):

    img = Image.open(img_path).convert('RGB')
    # print(img.height,img.width)

    # 计算要将原始图片粘贴到白色背景图上的位置,rotate or not
    rota=True if img.width < img.height * 0.95 else False

    if rota:
        img=rotate_image_90_no_crop(img,reverse=True)
    #     ht,wh=img.width, img.height
    #     print("Flipped!")
    # else:
    wh,ht  = img.width, img.height
    # print(img.height, img.width)
    # 计算新的图像尺寸
    new_width = tgt_size
    new_height = int(ht * new_width / wh)
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
    logo_img = Image.open(logo_file).convert('RGB')
    logo_height = infor_area * 0.8
    logo_img=logo_img.resize((int(logo_img.width*logo_height/logo_img.height),int(logo_height)))
    background.paste(logo_img,(int(tgt_size+2*border_size+exterior-logo_img.width*logo_height/logo_img.height),int(new_height+2*border_size+2*exterior)))
    draw = ImageDraw.Draw(background)
    # add text 1 the camera
    font = ImageFont.truetype("arial.ttf", font_size)
    posi = (exterior, 2 * exterior + new_height + 2*border_size)
    text_1=text.split('\n\n')[0]
    draw.text(posi, text_1, fill=(0, 0, 0), font=font)
    # mkae it bold
    bold_offset = 1
    for offset in [(0, 0), (bold_offset, 0), (0, bold_offset), (bold_offset, bold_offset)]:
        draw.text((posi[0] + offset[0], posi[1] + offset[1]), text_1, font=font, fill=(0, 0, 0))

    # add text 1 the lens
    font = ImageFont.truetype("arial.ttf", int(font_size*0.9))
    posi = (exterior, 2 * exterior + new_height + 2 * border_size+1.8*font_size)
    text_2 = text.split('\n\n')[1]
    draw.text(posi, text_2, fill=(0, 0, 0), font=font)
    # text2 = "\nShot in Somewhere on the earth."

    # add main_color
    main_c=extract_main_colors(img,num_colors=4)
    color_image = np.zeros((int(0.8* font_size), int(15*font_size), 3), dtype=int)

    block_width = color_image.shape[1] // len(main_c)

    for i, color in enumerate(main_c):
        color_image[:, i * block_width:(i + 1) * block_width] = color
    color_pad=Image.fromarray(color_image.astype('uint8'))
    posi_mc=(exterior, int(2 * exterior + new_height + 2 * border_size+3.4*font_size))
    background.paste(color_pad,posi_mc)

    # rotate back and save

    if rota:
        background=rotate_image_90_no_crop(background,reverse=False)
    dir_p=os.path.split(os.path.split(img_path)[0])[1]
    sav_path=os.path.join(tgt, dir_p+'_'+os.path.splitext(os.path.split(img_path)[1])[0] + f".jpg")
    # 保存最终结果os.path.join(tgt, os.path.splitext(os.path.split(img_path)[1])[0] + f".jpg")

    return background.save(sav_path)


if __name__=='__main__':
    if not os.path.exists(tgt):
        os.mkdir(tgt)

    # 加载原始图片

    dir_list=os.listdir(src)
    for dir_name in dir_list:
        if os.path.isdir(os.path.join(src,dir_name)) and dir_name in text_dict:
            text_line,logo_path=text_dict[dir_name]
            img_all = []
            for suf in ['png','jpeg','jpg','PNG','tif']:
                img_all.extend(glob.glob(os.path.join(src,dir_name,"*."+suf)))

            print(f'Images need to be processed: {img_all}')
            for indx in range(len(img_all)):
                print("\rProcessing line {}/{}...".format(indx+1, len(img_all)), end='', flush=True)
                process_res = process_one_image(img_all[indx],text=text_line,logo_file=logo_path)
