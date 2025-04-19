# install and start zinit
ZINIT_HOME="${XDG_DATA_HOME:-${HOME}/.local/share}/zinit/zinit.git"
[ ! -d $ZINIT_HOME ] && mkdir -p "$(dirname $ZINIT_HOME)"
[ ! -d $ZINIT_HOME/.git ] && git clone https://github.com/zdharma-continuum/zinit.git "$ZINIT_HOME"
source "${ZINIT_HOME}/zinit.zsh"

# load brew so brew installed commands are in the path
eval $(/opt/homebrew/bin/brew shellenv)

zinit light Aloxaf/fzf-tab
zinit light zsh-users/zsh-autosuggestions
zinit light zdharma-continuum/fast-syntax-highlighting
zinit light zsh-users/zsh-completions
# ensure this is after autosuggestions and syntax-highlighting
zinit light softmoth/zsh-vim-mode

autoload -U compinit && compinit

zinit cdreplay -q

# keybindings
# bindkey '^j' history-search-forward
# bindkey '^k' history-search-backward

# history settings
HISTSIZE=100000
HISTFILE=~/.zsh_history
SAVEHIST=$HISTSIZE
HISTDUP=erase
setopt appendhistory
setopt sharehistory
setopt hist_ignore_space
setopt hist_ignore_all_dups
setopt hist_save_no_dups
setopt hist_ignore_dups
setopt hist_find_no_dups

source ${HOME}/.aliases

# completion styling
zstyle ':completion:*' list-color "${(s.:.)LS_COLORS}"
zstyle ':completion:*' menu no
zstyle ':fzf-tab:complete:cd:*' fzf-preview 'eza $realpath'
zstyle ':fzf-tab:complete:__zoxide_z:*' fzf-preview 'eza $realpath'

eval "$(fzf --zsh)"
eval "$(zoxide init zsh)"
eval "$(starship init zsh)"
source ~/.orbstack/shell/init.zsh 2>/dev/null || :

# load OMZ plugins
zinit snippet OMZP::git
zinit snippet OMZP::brew
zinit snippet OMZP::direnv
zinit snippet OMZP::fzf
zinit snippet OMZP::gh
zinit snippet OMZP::uv

# setup ssh agent
zinit snippet OMZP::ssh-agent
zstyle :omz:plugins:ssh-agent quiet yes
zstyle :omz:plugins:ssh-agent lazy yes
zstyle :omz:plugins:ssh-agent agent-forwarding yes
zstyle :omz:plugins:ssh-agent identities ~/.ssh/id_ed25519

# stop zinit overloading `zi` alias (i.e. use zoxide's `zi`)
zinit wait lucid atload'_zsh_autosuggest_start; unalias zi' light-mode for \
    zsh-users/zsh-autosuggestions

zinit snippet ~/.zinit/tmux-sesh/sesh.zsh

