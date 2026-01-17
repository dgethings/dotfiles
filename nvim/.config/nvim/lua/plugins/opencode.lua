return {
  "NickvanDyke/opencode.nvim",
  dependencies = {
    -- Recommended for `ask()` and `select()`.
    -- Required for `snacks` provider.
    ---@module 'snacks' <- Loads `snacks.nvim` types for configuration intellisense.
    -- { "folke/snacks.nvim", opts = { input = {}, picker = {}, terminal = {} } },
    { "folke/snacks.nvim", opts = {} },
  },
  keys = {
    {
      "<C-a>",
      function()
        require("opencode").ask("@this: ", { submit = true })
      end,
      mode = { "n", "x" },
      desc = "Ask opencode...",
    },
    {
      "<C-x>",
      function()
        require("opencode").select()
      end,
      mode = { "n", "x" },
      desc = "Execute opencode action",
    },
    {
      "<C-.>",
      function()
        require("opencode").toggle()
      end,
      mode = { "n", "t" },
      desc = "Toggle opencode",
    },
    {
      "go",
      function()
        return require("opencode").operator("@this ")
      end,
      mode = { "n", "x" },
      desc = "Add range to opencode",
      expr = true,
    },
    {
      "goo",
      function()
        return require("opencode").operator("@this ") .. "_"
      end,
      mode = { "n", "x" },
      desc = "Add line to opencode",
      expr = true,
    },
    {
      "<S-C-u>",
      function()
        require("opencode").command("session.half.page.up")
      end,
      mode = "n",
      desc = "Scroll opencode up",
    },
    {
      "<S-C-d>",
      function()
        require("opencode").command("session.half.page.down")
      end,
      mode = "n",
      desc = "Scroll opencode down",
    },
    {
      "+",
      "<C-a>",
      mode = "n",
      desc = "Increment under cursor",
      noremap = true,
    },
    {
      "-",
      "<C-x>",
      mode = "n",
      desc = "Decrement under cursor",
      noremap = true,
    },
  },
  opts = {
    autoread = true,
    opencode_opts = { provider = { enabled = "tmux" } },
  },
}
