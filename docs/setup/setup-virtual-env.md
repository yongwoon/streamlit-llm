# Setup virtual env & use

- Install pyenv

```bash
brew update
brew install pyenv

# install python with version (ex: 3.11.11)
pyenv install 3.11.11

# set python version in local
pyenv local 3.11.11

pyenv versions
```

- set venv

```bash
python3.11 -m venv env
```

- virtual env コマンド

```bash
# activate env
source env/bin/activate

# deactivate
deactivate
```
