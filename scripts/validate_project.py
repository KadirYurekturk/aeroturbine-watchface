"""Validate the checked-in Redmi Watch 4 project without a compiler or device."""
from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import Image

root_dir=Path(__file__).resolve().parents[1]
folder=root_dir/'watchfaces'/'redmi-watch-4'
project=ET.parse(folder/'AeroTurbine.fprj').getroot()
assert project.get('DeviceType')=='365', 'Wrong target device'
widgets=project.find('Screen').findall('Widget')
assert len({w.get('Name') for w in widgets})==len(widgets)
sources={w.get('Value_Src') or w.get('Index_Src') for w in widgets}
assert {'0811','1011','1812','1012','2012','0821','0841','2031','3031'}<=sources
byname={w.get('Name'):w for w in widgets}
assert 'Weather unavailable' not in byname
icons=[byname[n] for n in ('Steps airplane icon','Battery missile icon','Weather conditions')]
assert [int(w.get('X'))+int(w.get('Width'))/2 for w in icons]==[73,195,317]
assert len({w.get('Y') for w in icons})==1
for w in widgets:
    x,y,width,height=(int(w.get(k)) for k in ('X','Y','Width','Height'))
    assert x>=0 and y>=0 and x+width<=390 and y+height<=450,w.get('Name')
    entries=w.get('BitmapList','').split('|') if w.get('BitmapList') else []
    filenames=[e.split(':',1)[-1] for e in entries]
    if w.get('Bitmap'):filenames.append(w.get('Bitmap'))
    for file in filenames:
        with Image.open(folder/'images'/file) as im: im.verify()
    if w.get('Shape')=='32':
        assert len(entries)==(11 if w.get('Value_Src')=='2031' else 10)
        with Image.open(folder/'images'/filenames[0]) as im:assert width==im.width*int(w.get('Digits'))
    if w.get('Index_Src')=='3031':assert len(entries)==42
for name in ('Hour weather color','Minute weather color'):
    entries={int(e.split('):')[0][1:]):e.split('):')[1] for e in byname[name].get('BitmapList').split('|')}
    for index,color in [(0,(255,203,72)),(7,(0,199,239)),(2,(250,250,250)),(40,(250,250,250))]:
        with Image.open(folder/'images'/entries[index]) as im:assert im.getpixel((0,0))[:3]==color
temp=byname['Temperature Celsius']
assert temp.get('Digits')=='3' and temp.get('Visible_Src')=='4'
datebottoms=[]
for name in ('Weekday','Day','Date separator','Month'):
    w=byname[name]
    file=(w.get('Bitmap') or w.get('BitmapList').split('|')[0]).split(':')[-1]
    with Image.open(folder/'images'/file) as im:datebottoms.append(int(w.get('Y'))+im.getchannel('A').getbbox()[3])
assert max(datebottoms)-min(datebottoms)<=1
with Image.open(folder/'images'/'thumbnail.png') as im:assert im.size==(234,270)
print('PASS: device, live sources, asset integrity, bounds, aligned date/icons, weather colors and signed temperature')
