# LangServeHub Project Template

## Installation
```bash
poetry install
```

## Adding packages
```bash
# if you have problems with `poe`, try `poetry run poe`

# adding packages from https://github.com/langchain-ai/langserve-hub
poe add simple/pirate

# adding custom GitHub repo packages
poe add --repo=hwchase17/chain-of-verification

# with a custom api mount point (defaults to `/{package_name}`)
poe add simple/translator --api_path=/my/custom/path/translator
```

## Removing packages

Note: you remove packages by their api path
```bash
poe remove pirate
```