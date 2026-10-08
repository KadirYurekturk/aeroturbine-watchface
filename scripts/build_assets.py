from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont, ImageChops

workspace = Path(__file__).resolve().parents[1]
folder = workspace / 'watchfaces' / 'redmi-watch-4'
images = folder / 'images'
images.mkdir(parents=True, exist_ok=True)
S = 3
FONT = 'C:/Windows/Fonts/arialbd.ttf'
WHITE, GRAY, ORANGE, CYAN = '#FAFAFA', '#93989E', '#FF9E00', '#00C7EF'
root = ET.Element('FaceProject', DeviceType='365', Id='167210071')
screen = ET.SubElement(root, 'Screen', Title='AeroTurbine', Bitmap='thumbnail.png')
layers = []

def tile(w, h): return Image.new('RGBA', (w*S, h*S), (0, 0, 0, 0))

def save(im, name):
    im.resize((im.width//S, im.height//S), Image.Resampling.LANCZOS).save(images / name)
    return name

def label(draw, xy, value, size, color=WHITE, anchor='lt'):
    draw.text(tuple(v*S for v in xy), value, font=ImageFont.truetype(FONT, size*S), fill=color, anchor=anchor)

def widget(shape, name, x, y, w, h, **attrs):
    return ET.SubElement(screen, 'Widget', Shape=str(shape), Name=name, X=str(x), Y=str(y),
                         Width=str(w), Height=str(h), Alpha='255', Visible_Src='0', **{k:str(v) for k,v in attrs.items()})

def static(name, filename, x, y, w, h):
    widget(30, name, x, y, w, h, Bitmap=filename)
    layers.append((filename, x, y))

def glyphs(prefix, w, h, size, color=WHITE, heavy=False, minus=False, baseline=None):
    result = []
    font = ImageFont.truetype('C:/Windows/Fonts/ariblk.ttf' if heavy else FONT, size*S)
    for n in list('0123456789') + (['-'] if minus else []):
        im = tile(w, h)
        d = ImageDraw.Draw(im)
        bbox = d.textbbox((0, 0), n, font=font)
        gw, gh = bbox[2]-bbox[0], bbox[3]-bbox[1]
        glyph = Image.new('RGBA', (gw, gh), (0,0,0,0))
        ImageDraw.Draw(glyph).text((-bbox[0], -bbox[1]), n, font=font, fill=color)
        # Large clock numerals use the selected reference's tall block proportions.
        if heavy:
            glyph = glyph.resize(((w-5)*S, (h-7)*S), Image.Resampling.LANCZOS)
        elif gw > (w-1)*S:
            glyph = glyph.resize(((w-1)*S, gh), Image.Resampling.LANCZOS)
        if baseline is not None:
            ImageDraw.Draw(im).text(((w*S-font.getlength(n))/2,baseline*S),n,font=font,fill=color,anchor='ls')
        else:
            im.alpha_composite(glyph, ((im.width-glyph.width)//2, (im.height-glyph.height)//2))
        if heavy:
            # Inverse-alpha native number tiles reveal the weather-driven color beneath.
            mask = Image.new('RGBA', im.size, 'black')
            mask.putalpha(ImageChops.invert(im.getchannel('A')))
            im = mask
        result.append(save(im, f'{prefix}{n if n != "-" else "minus"}_rgba.png'))
    return result

def number(name, source, names, x, y, count, w, h, sample, hide=False, align=0, valid=False):
    a = widget(32, name, x, y, count*w, h, BitmapList='|'.join(names), Value_Src=source,
               Digits=count, Alignment=align, Spacing=0, Blanking=int(hide))
    if valid: a.set('Visible_Src', '4')
    value = str(sample).zfill(count) if not hide else str(sample)
    offset = (count-len(value))*w//2 if align == 1 else ((count-len(value))*w if align == 2 else 0)
    for i,n in enumerate(value): layers.append((names[10 if n == '-' else int(n)], x+offset+i*w, y))

def image_list(name, source, names, x, y, w, h, sample=0, valid=False):
    a = widget(31, name, x, y, w, h, BitmapList='|'.join(f'({i}):{n}' for i,n in enumerate(names)),
               Index_Src=source, DefaultIndex=0)
    if valid: a.set('Visible_Src','4')
    layers.append((names[sample], x, y))

asset = workspace / 'assets' / 'engine-background.png'
bg = Image.open(asset).convert('RGB').resize((390,450), Image.Resampling.LANCZOS)
bg.save(images / 'background.png')
static('Engine fan', 'background.png', 0,0,390,450)

# Existing native widgets can combine weather color fields and live number masks.
# No scripting or conditional expressions are needed on the watch.
rain_indices={3,4,5,6,7,8,9,10,11,12,19,21,22,23,24,25,41}
color_files={}
for key,color in [('sun','#FFCB48'),('rain',CYAN),('neutral',WHITE)]:
    im=Image.new('RGB',(136*S,109*S),color)
    color_files[key]=save(im,f'clock-color-{key}.png')
clock_colors=[color_files['sun' if i==0 else 'rain' if i in rain_indices else 'neutral'] for i in range(42)]
for name,y in [('Hour',45),('Minute',157)]:
    image_list(name+' weather color','3031',clock_colors,12,y,136,109,0)
    invalid=widget(30,name+' color when weather unavailable',12,y,136,109,Bitmap=color_files['neutral'])
    invalid.set('Visible_Src','1')
clock = glyphs('clock', 68, 109, 140, heavy=True)
number('Hour','0811',clock,12,45,2,68,109,9)
number('Minute','1011',clock,12,157,2,68,109,28)
date = glyphs('date', 13,22,20,GRAY,baseline=17)
weeks = []
for i,v in enumerate(['PAZ','PZT','SAL','ÇAR','PER','CUM','CMT']):
    im = tile(45,22); label(ImageDraw.Draw(im),(0,17),v,19,GRAY,'ls')
    weeks.append(save(im,f'week{i}_rgba.png'))
image_list('Weekday','2012',weeks,14,287,45,22,4)
number('Day','1812',date,64,287,2,13,22,8)
im=tile(9,22); label(ImageDraw.Draw(im),(0,17),'/',20,GRAY,'ls')
static('Date separator',save(im,'date-slash_rgba.png'),93,287,9,22)
number('Month','1012',date,106,287,2,13,22,10)

def library_icon(name):
    size=40
    return Image.open(workspace/'assets'/'icons'/(name+'.png')).convert('RGBA').resize((size*S,size*S),Image.Resampling.LANCZOS)

icon_size=40
icon_y=351
static('Steps airplane icon',save(library_icon('plane'),'airplane_rgba.png'),73-icon_size//2,icon_y,icon_size,icon_size)
static('Battery missile icon',save(library_icon('rocket'),'missile_rgba.png'),195-icon_size//2,icon_y,icon_size,icon_size)
metric_font=30
steps=glyphs('step',20,34,metric_font)
number('Steps','0821',steps,23,390,5,20,34,8246,True,1)
battery=glyphs('battery',20,34,metric_font)
number('Battery','0841',battery,165,390,3,20,34,78,True,1)

def weather_icon(kind):
    name={'sun':'sun','partly':'cloud','cloud':'cloud','rain':'cloud-rain','storm':'cloud-storm',
          'snow':'cloud-snow','sleet':'cloud-snow','fog':'cloud-fog','dust':'wind','wind':'wind','unknown':'cloud-off'}[kind]
    return library_icon(name+'-accent')

# Indices follow EasyFace's documented WeatherTableIT (0 through 41).
kinds=['sun','partly','cloud','rain','storm','sleet','sleet','rain','rain','rain','storm','rain','storm',
       'snow','snow','snow','snow','snow','fog','sleet','dust','rain','rain','storm','rain','rain',
       'snow','snow','snow','dust','wind','dust','fog','fog','fog','fog','fog','fog','fog','fog','unknown','rain']
weather=[save(weather_icon(kind),f'weather{i}_rgba.png') for i,kind in enumerate(kinds)]
image_list('Weather conditions','3031',weather,317-icon_size//2,icon_y,icon_size,icon_size,0,True)
temp=glyphs('temperature',20,34,metric_font,minus=True)
temp_x=272
unit_x=333
number('Temperature Celsius','2031',temp,temp_x,390,3,20,34,25,True,2,True)
im=tile(14,34); label(ImageDraw.Draw(im),(0,3),'°',18)
unit=widget(30,'Celsius unit',unit_x,390,14,34,Bitmap=save(im,'celsius_rgba.png')); unit.set('Visible_Src','4')
layers.append(('celsius_rgba.png',unit_x,390))

ET.indent(root,space='  ')
ET.ElementTree(root).write(folder/'AeroTurbine.fprj',encoding='utf-8',xml_declaration=True)
preview=Image.new('RGBA',(390,450),'black')
for filename,x,y in layers:
    with Image.open(images/filename) as im:preview.alpha_composite(im.convert('RGBA'),(x,y))
preview.convert('RGB').save(folder/'preview.png')
preview.convert('RGB').resize((234,270),Image.Resampling.LANCZOS).save(images/'thumbnail.png')
for weather_state,filename in [(0,'preview-sunny.png'),(7,'preview-rainy.png'),(2,'preview-cloudy.png')]:
    variant=Image.new('RGBA',(390,450),'black')
    for filename_layer,x,y in layers:
        if filename_layer.startswith('clock-color-'): filename_layer=clock_colors[weather_state]
        elif filename_layer.startswith('weather') and filename_layer.endswith('_rgba.png'): filename_layer=weather[weather_state]
        with Image.open(images/filename_layer) as im: variant.alpha_composite(im.convert('RGBA'),(x,y))
    variant.convert('RGB').save(folder/filename)
print(folder / 'AeroTurbine.fprj')
