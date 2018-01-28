# yeelight-gsi
Changing light scenes on Yeelight smart lamps for different in-game scenarios in Valve games using game state integration.

## Prerequisites
- Python 2.7 and above
- CS:GO or Dota 2 on Steam
- Any Yeelight/Xiaomi/Mijia Wi-Fi lamp

## Usage
To control your Yeelights via local network, you need to enable the [developer mode](https://www.yeelight.com/en_US/developer) (also called LAN mode) on your lamps in the Yeelight app.
Set your lamp's IP addresses in the config.ini.
Copy the gamestate_integration_yeelight.cfg to the corresponding `gamedir/cfg` folder. Run your `gsi-xxxx.py` of choice and launch the game.

## TODO

### CSGO 
- [x] Round state colors
- [x] Bomb state colors
- [X] Multiple lamp support
- [ ] Player health colors
- [ ] Bomb flashing

### Dota 2
- [X] Day time scenes
- [ ] Ult/Ability scenes (`CanCast, IsActive, Cooldown, ...`)
- [ ] Player state scenes (`IsSilenced, IsStunned, HasDebuff, IsHexed, ...`)
*Note: I'm not a Dota player myself so I don't know what features might be desirable. Feel free to get in touch via the issue section for suggestions. Same for CS:GO of course.*

## Credits
Gratefully using the [Yeelight python library](https://github.com/skorokithakis/python-yeelight/) by Stavros Korokithakis.  
Copyright (c) 2016, Stavros Korokithakis  
All rights reserved.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
