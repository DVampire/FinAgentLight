# FinAgentLight

## Install
```bash
create -n finagent_light python=3.12.0
conda activate finagent_light

# install poetry
curl -sSL https://install.python-poetry.org | python3 -
poetry install
```

## Dev
```bash
# install
make install

# configure pre-commit
pre-commit install --config dev_config/python/.pre-commit-config.yaml
```
