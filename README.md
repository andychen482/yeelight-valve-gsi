# yeelight-gsi
Changing light scenes on Yeelight smart lamps for different in-game scenarios in Valve games using game state integration.

## Prerequisites
- Windows (standalone) or Linux (python3 installed)
- CS:GO or Dota 2 on Steam
- Any Yeelight/Xiaomi/Mijia Wi-Fi lamp

## Usage
* Windows: Download the latest  binary from [releases](https://github.com/davidramiro/yeelight-gsi/releases)
* Linux: Clone the repo.
To control your Yeelights via local network, you need to enable the [developer mode](https://www.yeelight.com/en_US/developer) (also called LAN mode) on your lamps in the Yeelight app.
Set your lamp's IP addresses in the config.ini.
Copy the `gamestate_integration_yeelight.cfg` from the `cfg` directory to the corresponding game folder. For CS:GO that would be `gamedir/csgo/cfg` and for Dota 2 it goes into `gamedir/game/dota/cfg/gamestate_integration`. Run your `gsi-xxxx` executable of choice and launch the game.

## TODO

### CSGO 
- [x] Round state colors
- [x] Bomb state colors
- [X] Multiple lamp support
- [X] Player health colors and warning
- [X] Bomb flashing
- [ ] Ammo warning

### Dota 2
- [X] Player health scenes
- [ ] Ult/Ability scenes (`CanCast, IsActive, Cooldown, ...`)
- [ ] More player state scenes (`IsSilenced, IsStunned, HasDebuff, IsHexed, ...`)
*Note: I'm not a Dota player myself so I don't know what features might be desirable. Feel free to get in touch via the issue section for suggestions. Same for CS:GO of course.*

## Credits
Gratefully using the [Yeelight python library](https://github.com/skorokithakis/python-yeelight/) by Stavros Korokithakis.  
Copyright (c) 2016, Stavros Korokithakis  
All rights reserved.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
