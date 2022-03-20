# Installation
```sh
git clone https://github.com/pcroland/nfopng
cd nfopng
pip install -r requirements.txt
```
# Usage
```ruby
❯ ./nfopng.py
usage: nfopng.py [-h] [-v] [-i INPUT] [-o OUTPUT] [-min MIN] [-max MAX]
                 [-b BORDER] [-dcb] [-dcl] [-f FONT] [-lf]

options:
  -h, --help                     shows this help message.
  -v, --version                  shows version.
  -i INPUT, --input INPUT        NFO input file
  -o OUTPUT, --output OUTPUT     PNG output file
                                 default: input with .png suffix, or stdout if input is stdin
  -min MIN                       minimum brightness
                                 default: 30
  -max MAX                       minimum brightness
                                 default: 200
  -b BORDER, --border BORDER     border on image
                                 default: 4
  -dcb, --disable-custom-blocks  disable custom "░▒▓█▀▄▌▐" characters.
  -dcl, --disable-custom-lines   disable custom "■┌┐└┘─│" characters.
  -f FONT, --font FONT           font to use
                                 default: FiraCode
  -lf, --list-fonts              list fonts
```
