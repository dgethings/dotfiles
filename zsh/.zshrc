# install and start zinit
ZINIT_HOME="${XDG_DATA_HOME:-${HOME}/.local/share}/zinit/zinit.git"
[ ! -d $ZINIT_HOME ] && mkdir -p "$(dirname $ZINIT_HOME)"
[ ! -d $ZINIT_HOME/.git ] && git clone https://github.com/zdharma-continuum/zinit.git "$ZINIT_HOME"
export PATH=${PATH}:/opt/homebrew/bin
source "${ZINIT_HOME}/zinit.zsh"

# faster way to use eval during startup
# uses z-c/null as the light/load "drink" to add the ice to
zinit light NICHOLAS85/z-a-eval
# load brew so brew installed commands are in the path
zinit ice id-as"brew_init" has"brew" \
  eval"/opt/homebrew/bin/brew shellenv"
zinit light zdharma-continuum/null

# improved startup performance from fast-syntax-highlighting install instructions in repo
zinit wait lucid for \
  atinit"ZINIT[COMPINIT_OPTS]=-C; zicompinit; zicdreplay" \
    zdharma-continuum/fast-syntax-highlighting \
  blockf \
    zsh-users/zsh-completions \

# stop zinit overloading `zi` alias (i.e. use zoxide's `zi`)
zinit wait lucid atload'_zsh_autosuggest_start; unalias zi' light-mode for \
    zsh-users/zsh-autosuggestions

# faster direnv initialization
zinit from"gh-r" as"program" mv"direnv* -> direnv" \
    atclone'./direnv hook zsh > zhook.zsh' atpull'%atclone' \
    pick"direnv" src="zhook.zsh" for \
        direnv/direnv

zinit light Aloxaf/fzf-tab

# for what I need, this is enough vim mode in my shell
# and is much faster to start than softmoth/zsh-vim-mode
bindkey -v

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

# I use brew to install these
# so use z-a-eval to efficiently add completions
zinit ice id-as"fzf_load" has"fzf" \
  eval"fzf --zsh" run-atpull
zinit light zdharma-continuum/null
zinit ice id-as"init" has"zoxide" \
  eval"zoxide init zsh"
zinit light zdharma-continuum/null
zinit ice id-as"starship_init" has"starship" \
  eval"starship init zsh"
zinit light zdharma-continuum/null
source ~/.orbstack/shell/init.zsh 2>/dev/null || :
zinit ice id-as"orbctl_completion" has"orbctl" \
  eval"orbctl completion zsh"
zinit light zdharma-continuum/null
zinit ice id-as"orbctl_completion" has"orbctl" \
  eval"devpod completion zsh"
zinit light zdharma-continuum/null

# load OMZ plugins
zinit wait lucid for \
  OMZP::git \
  OMZP::brew \
  OMZP::direnv \
  OMZP::fzf \
  OMZP::gh \
  OMZP::uv

# setup ssh agent
zinit snippet OMZP::ssh-agent
zstyle :omz:plugins:ssh-agent quiet yes
zstyle :omz:plugins:ssh-agent lazy yes
zstyle :omz:plugins:ssh-agent agent-forwarding yes
zstyle :omz:plugins:ssh-agent identities ~/.ssh/id_ed25519

zinit snippet ~/.zinit/tmux-sesh/sesh.zsh


# Added by LM Studio CLI (lms)
export PATH="$PATH:/Users/dgethings/.lmstudio/bin"
# End of LM Studio CLI section

