# yeelight-gsi
Changing light scenes on Yeelight smart lamps for different in-game scenarios in CS:GO. With a few minor alterations to the parsed states it would be fully compatible with Dota 2 aswell.

## Prerequisites
- Python 2.7 and above
- CS:GO on Steam
- Any Yeelight/Xiaomi/Mijia Wi-Fi lamp

## Usage
To control your Yeelights via local network, you need to enable the [developer mode](https://www.yeelight.com/en_US/developer) (also called LAN mode) on your lamps in the Yeelight app.
Set your lamp's IP addresses in the config.ini.
Copy gamestate_integration_yeelight.cfg to your CSGO/cfg directory. Run gsi.py and launch CS:GO.

## TODO

- [x] Round state colors
- [x] Bomb state colors
- [X] Multiple lamp support
- [ ] Player health colors
- [ ] Bomb flashing


## Credits
Gratefully using the [Yeelight python library](https://github.com/skorokithakis/python-yeelight/) by Stavros Korokithakis.  
Copyright (c) 2016, Stavros Korokithakis  
All rights reserved.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
