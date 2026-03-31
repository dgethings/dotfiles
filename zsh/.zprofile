export EDITOR='nvim'
export TERM=xterm-ghostty
export BUN_INSTALL="$HOME/.bun"
export PATH="${BUN_INSTALL}/bin:${PATH}:${HOME}/.cargo/bin:${HOME}/.local/bin:/Applications/Obsidian.app/Contents/MacOS"
export FZF_DEFAULT_OPTS=$FZF_DEFAULT_OPTS'
    --color=fg:#e5e9f0,bg:#3b4252,hl:#81a1c1
    --color=fg+:#e5e9f0,bg+:#3b4252,hl+:#81a1c1
    --color=info:#eacb8a,prompt:#bf6069,pointer:#b48dac
    --color=marker:#a3be8b,spinner:#b48dac,header:#a3be8b'
export VAULT_PATH="/Users/dgethings/Library/Mobile Documents/iCloud~md~obsidian/Documents/Main"

# Added by LM Studio CLI (lms)
export PATH="$PATH:/Users/dgethings/.lmstudio/bin"
# End of LM Studio CLI section

# bun completions
[ -s "/Users/dgethings/.bun/_bun" ] && source "/Users/dgethings/.bun/_bun"

# OpenClaw Completion
source "/Users/dgethings/.openclaw/completions/openclaw.zsh"

# Added by OrbStack: command-line tools and integration
# This won't be added again if you remove it.
# source ~/.orbstack/shell/init.zsh 2>/dev/null || :

# Added by `rbenv init` on Sun 20 Jul 2025 13:48:08 BST
# eval "$(rbenv init - --no-rehash zsh)"
source ~/.secrets

