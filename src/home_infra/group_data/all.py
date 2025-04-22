"""
Common data for all hosts.
"""

# User to create during first boot
user = "admin"

# Packages to install on all hosts
common_packages = [
    "zsh",
    "ripgrep",
    "fd-find",
    "fzf",
    "kitty-terminfo",
    "docker.io",
]

# Shell configuration
shell = {
    "default": "zsh",
    "prompt": "starship",
}

# SSH configuration
ssh = {
    "port": 22,
    "permit_root_login": "no",
    "password_authentication": "no",
}
