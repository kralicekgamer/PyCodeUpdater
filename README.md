# PyCodeUpdater
## Info
- This is a script that can update the code to the latest version
- Work with github

## File legend
- `config.ini` - configuration file
- `updater.py` - main file
- `example.py` - example script

## Install
### Instalation on GitHub
- Create file on github, which will be called `version`
- Type in this file your lasted version (`1.0` or `v1.0`)
- Create relese with tag `1.0` or `v1.0` on your github


### Instalation in you program
- Download lasted relese or download `updater.py` and `config.ini`
- Add this to you program
```
# import updater
from updater import Start

# call class Start
Start()
```
