# Dotfiles

This uses stow structure as suggested [here](https://gist.github.com/andreibosco/cb8506780d0942a712fc).

If you clone this repo to a dir other than `$HOME` then you'll need to supply the `-t ~` option to `stow` for this to work.

## Install files & software

Each of the dotfiles is structured under a directory. For example, to install the zsh dotfiles run:

```bash
stow -t ~ zsh
```

From the root of this repo.

To install the `brew` packages run:

```bash
brew bundle install
```
