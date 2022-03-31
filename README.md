# openconnect-sso

Wrapper script for OpenConnect supporting Azure AD (SAMLv2) authentication
to Cisco SSL-VPNs

This is a fork of a [fork](https://github.com/mgagliardo91/openconnect-sso/tree/custom-scripts) of [openconnect-sso](https://github.com/vlaci/openconnect-sso).  This removes the QT5 requirement and replaces it with Selenium.  This greatly increases the ease of using openconnect on Apple Silicon due to Qt5 being unsupported.  It also allows the use of openconnect-sso inside a docker container with custom scripting. 

The only purpose of this fork is to add some simple documentation on how to get this working, particularly on M1 Macs.


## Installation

### MacOS - Apple Silicon

#### Pre install setup

You will need openconnect first - the easiest is to install via brew
```shell
brew install openconnect
```

You will also need chrome or chromium browser.

#### Using pip/pipx

A generic way that works on most 'standard' Linux distributions out of the box.
The following example shows how to install `openconect-sso` along with its
dependencies including Qt:

```shell
$ pip install --user pipx # use brew install pip if pip not installed
Successfully installed pipx
$ pipx install "https://github.com/mgagliardo91/openconnect-sso/archive/refs/heads/custom-scripts.zip"
⣾ installing openconnect-sso
  installed package openconnect-sso 0.4.0, Python 3.7.5
  These apps are now globally available
    - openconnect-sso
⚠️  Note: '/home/vlaci/.local/bin' is not on your PATH environment variable.
These apps will not be globally accessible until your PATH is updated. Run
`pipx ensurepath` to automatically add it, or manually modify your PATH in your
shell's config file (i.e. ~/.bashrc).
done! ✨ 🌟 ✨
Successfully installed openconnect-sso
$ pipx ensurepath
Success! Added /home/vlaci/.local/bin to the PATH environment variable.
Consider adding shell completions for pipx. Run 'pipx completions' for
instructions.

You likely need to open a new terminal or re-login for the changes to take
effect. ✨ 🌟 ✨
```

Of course you can also install via `pip` instead of `pipx` if you'd like to
install system-wide or a virtualenv of your choice.

## Usage

If you want to save credentials and get them automatically
injected in the web browser:

```shell
$ openconnect-sso --server vpn.server.com/group --user user@domain.com --authenticate-timeout 120 
Password (user@domain.com):
[info     ] Authenticating to VPN endpoint ...
```
authenticate-timeout is optional, the default is 10s which can make entering details tricky.

User credentials are automatically saved to the users login keyring (if
available).

If you already have Cisco AnyConnect set-up, then `--server` argument is
optional. Also, the last used `--server` address is saved between sessions so
there is no need to always type in the same arguments:

```shell
$ openconnect-sso
[info     ] Authenticating to VPN endpoint ...
```

Configuration is saved in `$XDG_CONFIG_HOME/openconnect-sso/config.toml`. On
typical Linux installations it is located under
`$HOME/.config/openconnect-sso/config.toml`

Example configuration (generated on first run):

```toml
on_disconnect = ""
override_script = ""
authenticate_timeout = 10

[default_profile]
address = ""
user_group = ""
name = ""

[credentials]
username = ""

[auto_fill_rules]
[[auto_fill_rules."https://*"]]
selector = "div[id=passwordError]"
action = "stop"

[[auto_fill_rules."https://*"]]
selector = "input[type=email]"
fill = "username"

[[auto_fill_rules."https://*"]]
selector = "input[type=password]"
fill = "password"

[[auto_fill_rules."https://*"]]
selector = "input[type=submit]"
action = "click"
```

## Custom SSO script

openconnect-sso uses [Selenium](https://selenium-python.readthedocs.io/) to interface with the browser in order to automate entering the credentials required to achieve an access token for connecting with `openconnect`.

If the `auto_fill_rules` in the _config.toml_ file do not meet the needs of your usage, the path to a custom javascript userscript can be passed via the argument `--override-script` or in the configuration by specifying a value for `override_script`.

This file is expanded with environment variables including `USERNAME` and `PASSWORD` to enable the same script to be applied across unique logins.

An example of the a script is located at [example/defaultRules.js](./example/defaultRules.js). This example is the same script that is executed with the default `auto_fill_rules`.

## Headless-Mode

Headless usage can be specified using the argument `--browser-display-mode=hidden`. In this mode, the browser will not be displayed while the script interacts with the SSO provider. This mode can also be used to enable support for containerized environments

### Debugging Headless Execution

When running in headless mode, any failures in attempting to authenticate in the browser will attempt to be captured in a screenshot which will be saved to the current working directory.


## Development

`openconnect-sso` is developed using [Nix](https://nixos.org/nix/). Refer to the
[Quick Start section of the Nix
manual](https://nixos.org/nix/manual/#chap-quick-start) to see how to get it
installed on your machine.

To get dropped into a development environment, just type `nix-shell`:

```shell
$ nix-shell
Sourcing python-catch-conflicts-hook.sh
Sourcing python-remove-bin-bytecode-hook.sh
Sourcing pip-build-hook
Using pipBuildPhase
Sourcing pip-install-hook
Using pipInstallPhase
Sourcing python-imports-check-hook.sh
Using pythonImportsCheckPhase
Run 'make help' for available commands

[nix-shell]$
```

To try an installed version of the package, issue `nix-build`:

```shell
$ nix build
[1 built, 0.0 MiB DL]

$ result/bin/openconnect-sso --help
```

Alternatively you may just [get Poetry](https://python-poetry.org/docs/) and
start developing by using the included `Makefile`. Type `make help` to see the
possible make targets.
