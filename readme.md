# CollectQT Website

Debug mode

    python webapp/main.py

Production mode

    foreman start

## Installation

### OSX

```
brew install pyenv
pyenv install 3.4.3
virtualenv --python=python3.4 .venv
source .venv/bin/activate
pip install -r requirements.txt
python webapp/main.py
```
