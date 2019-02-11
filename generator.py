from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from random import randrange, uniform

char_len = 6
char_width = 48
char_height = char_width + 10
font_size = 32

char_set = [chr(c) for c in range(ord('a'), ord('z') + 1)]
char_set.extend([chr(c) for c in range(ord('A'), ord('Z') + 1)])
char_set.extend([chr(c) for c in range(ord('0'), ord('9') + 1)])
set_len = len(char_set)

captcha_size = (char_len * char_width, char_height)
captcha_img = Image.new('RGB', captcha_size, 'white')

trans_offset = 15

point_number = 20
point_radius = 2

line_number = 3
line_width = 3

ans = []


def rand_rgb():
    return randrange(0, 200), randrange(0, 200), randrange(0, 200)


def draw_points():
    for i in range(point_number):
        x, y = randrange(0, captcha_size[0]), randrange(0, captcha_size[1])
        draw = ImageDraw.Draw(captcha_img)
        draw.ellipse((x - point_radius, y - point_radius, x + point_radius, y + point_radius), fill=rand_rgb())


def draw_lines():
    for i in range(line_number):
        x1, y1 = randrange(0, captcha_size[0]), randrange(0, captcha_size[1])
        x2, y2 = randrange(0, captcha_size[0]), randrange(0, captcha_size[1])
        draw = ImageDraw.Draw(captcha_img)
        draw.line((x1, y1, x2, y2), rand_rgb(), width=line_width)


def draw_captcha_char():
    for i in range(char_len):
        sub_img = Image.new('RGBA', (char_width - trans_offset, char_height - trans_offset), 'white')
        draw = ImageDraw.Draw(sub_img)
        font = ImageFont.truetype('arial.ttf', font_size)
        ans.append(char_set[randrange(0, set_len)])
        draw.text((0, 0), ans[-1], font=font,
                  fill=rand_rgb())
        # 仿射变换，参数可以继续调优
        sub_img = sub_img.transform((char_width, char_height), Image.AFFINE,
                                    (1, uniform(-0.4, 0.4), -15, uniform(-0.3, 0.3), 1, -5))
        blank_img = Image.new('RGBA', sub_img.size, (255,) * 4)
        sub_img = Image.composite(sub_img, blank_img, sub_img)
        # sub_img.show()
        captcha_img.paste(sub_img, (i * char_width, 0, (i + 1) * char_width, char_height))


draw_captcha_char()
draw_points()
draw_lines()
captcha_img.show()
captcha_img.save('demo.jpg')

print(ans)
