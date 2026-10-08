"""Package the compiled .face and editable source; never bundle the compiler."""
from pathlib import Path
import hashlib
import xml.etree.ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED

repo=Path(__file__).resolve().parents[1]
version='v0.1.0'
project=repo/'watchfaces'/'redmi-watch-4'
root=ET.parse(project/'AeroTurbine.fprj').getroot()
assert root.get('DeviceType')=='365'
identifier=root.get('Id').encode('ascii')
assert len(identifier)==9 and identifier.isdigit()
face=repo/'.build'/'AeroTurbine.face'
data=bytearray(face.read_bytes())
assert len(data)>49
# Match Mi Create's FPRJ project-ID update in the compiled header.
data[40:49]=identifier
face.write_bytes(data)
dist=repo/'dist'
dist.mkdir(exist_ok=True)
binary=dist/f'AeroTurbine-RedmiWatch4-{version}.bin'
binary.write_bytes(data)
archive=dist/f'AeroTurbine-RedmiWatch4-{version}-editable.zip'
with ZipFile(archive,'w',ZIP_DEFLATED) as out:
    out.write(project/'AeroTurbine.fprj','watchfaces/redmi-watch-4/AeroTurbine.fprj')
    for file in sorted((project/'images').glob('*.png')):
        out.write(file,file.relative_to(repo))
    for file in ['README.md','README.tr.md','LICENSE','docs/ASSETS.md','docs/COMPATIBILITY.md','licenses/Tabler-Icons-MIT.txt']:
        out.write(repo/file,file)
    for file in sorted((repo/'docs'/'previews').glob('*.png')):
        out.write(file,file.relative_to(repo))
checksum=dist/'SHA256SUMS.txt'
checksum.write_text(''.join(f'{hashlib.sha256(file.read_bytes()).hexdigest()}  {file.name}\n' for file in [binary,archive]),encoding='utf-8')
print(f'Created {binary.name}, {archive.name}, {checksum.name}')
