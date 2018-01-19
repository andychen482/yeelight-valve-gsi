# yeelight-gsi
Changing light scenes on Yeelight smart lamps for different in-game scenarios in CS:GO. With a few minor alterations to the parsed states it would be fully compatible with Dota 2 aswell.

## Prerequisites
- Python
- CS:GO on Steam
- Any Yeelight/Xiaomi/Mijia Wi-Fi lamp

## Usage
To control your Yeelight via local network, you need to enable the [developer mode](https://www.yeelight.com/en_US/developer) (also called LAN mode) on your lamp in the Yeelight app.
Set your lamp's IP address in the config.ini.
Copy gamestate_integration_yeelight.cfg to your CSGO/cfg directory. Run gsi.py and launch CS:GO.

## TODO

- [x] Round state colors
- [x] Bomb state colors
- [ ] Player health colors
- [ ] Bomb flashing
- [ ] Multiple lamp support

## Credits
Gratefully using the Yeelight python library by Stavros Korokithakis.

https://github.com/skorokithakis/python-yeelight/

Copyright (c) 2016, Stavros Korokithakis

All rights reserved.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
