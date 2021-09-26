# juypterlab_sparkui_tab

[![Github Actions Status](https://github.com/rajatonit/juypterlab-sparkui-tab/workflows/Build/badge.svg)](https://github.com/rajatonit/juypterlab-sparkui-tab/actions/workflows/build.yml)[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/rajatonit/juypterlab-sparkui-tab/main?urlpath=lab)

Finds where sparkui is running and creates a proxy to it


This extension is composed of a Python package named `juypterlab_sparkui_tab`
for the server extension and a NPM package named `juypterlab-sparkui-tab`
for the frontend extension.


## Requirements

* JupyterLab >= 3.0

## Install

To install the extension, execute:

```bash
pip install juypterlab_sparkui_tab
```

## Uninstall

To remove the extension, execute:

```bash
pip uninstall juypterlab_sparkui_tab
```


## Troubleshoot

If you are seeing the frontend extension, but it is not working, check
that the server extension is enabled:

```bash
jupyter server extension list
```

If the server extension is installed and enabled, but you are not seeing
the frontend extension, check the frontend extension is installed:

```bash
jupyter labextension list
```


## Contributing

### Development install

Note: You will need NodeJS to build the extension package.

The `jlpm` command is JupyterLab's pinned version of
[yarn](https://yarnpkg.com/) that is installed with JupyterLab. You may use
`yarn` or `npm` in lieu of `jlpm` below.

```bash
# Clone the repo to your local environment
# Change directory to the juypterlab_sparkui_tab directory
# Install package in development mode
pip install -e .
# Link your development version of the extension with JupyterLab
jupyter labextension develop . --overwrite
# Server extension must be manually installed in develop mode
jupyter server extension enable juypterlab_sparkui_tab
# Rebuild extension Typescript source after making changes
jlpm run build
```

You can watch the source directory and run JupyterLab at the same time in different terminals to watch for changes in the extension's source and automatically rebuild the extension.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
jlpm run watch
# Run JupyterLab in another terminal
jupyter lab
```

With the watch command running, every saved change will immediately be built locally and available in your running JupyterLab. Refresh JupyterLab to load the change in your browser (you may need to wait several seconds for the extension to be rebuilt).

By default, the `jlpm run build` command generates the source maps for this extension to make it easier to debug using the browser dev tools. To also generate source maps for the JupyterLab core extensions, you can run the following command:

```bash
jupyter lab build --minimize=False
```

### Development uninstall

```bash
# Server extension must be manually disabled in develop mode
jupyter server extension disable juypterlab_sparkui_tab
pip uninstall juypterlab_sparkui_tab
```

In development mode, you will also need to remove the symlink created by `jupyter labextension develop`
command. To find its location, you can run `jupyter labextension list` to figure out where the `labextensions`
folder is located. Then you can remove the symlink named `juypterlab-sparkui-tab` within that folder.

### Packaging the extension

See [RELEASE](RELEASE.md)
