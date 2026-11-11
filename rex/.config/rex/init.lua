-- Rex keybindings migrated from tmux and Herdr (Ghostty contributed no bindings).
-- Prefix: ctrl+s

-- tmux.conf:14  bind | split-window -h  (Herdr config.toml:14 split_vertical binds
-- the same key; tmux won, and both translate to the same binding)
rex.bind("ctrl+s>shift+\\", "pane.split", { direction = "right" })

-- tmux.conf:15  bind - split-window -v  (Herdr config.toml:15 split_horizontal binds
-- the same key; tmux won, and both translate to the same binding)
rex.bind("ctrl+s>-", "pane.split", { direction = "down" })

-- tmux.conf:22  bind-key C-s send-prefix
rex.bind("ctrl+s>ctrl+s", "pane.send_key", { key = "ctrl+s" })

-- tmux.conf:28  bind c new-window
rex.bind("ctrl+s>c", "client.tab.new")

-- tmux.conf:73  bind-key x kill-pane
rex.bind("ctrl+s>x", "pane.close")
