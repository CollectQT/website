# CollectQT Website

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

## Running

Debug mode

    python webapp/main.py

Production mode

    foreman start

## Cleanup

    autopep8 --in-place --aggressive --aggressive -r webapp/

    npm install -g stylelint stylefmt
    npm install stylelint-config-standard --save-dev
    stylefmt -r webapp/static/scss/*
