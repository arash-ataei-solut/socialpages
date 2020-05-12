from PIL import Image

a = 'yes'
while a == 'yes':
    file_name = str(input('enter png file name: '))
    im = Image.open(file_name)
    width = int(input('enter width: '))
    if im.size[0] > im.size[1]:
        size = int(im.size[0]*width/im.size[1]), width
    else:
        size = width, int(im.size[1]*width/im.size[0])
    im_resized = im.resize(size, Image.ANTIALIAS)
    im_resized.save(str(input('enter new file name: ')) + '.png', "PNG")
    a = str(input('do you want to continue? ')).lower()
