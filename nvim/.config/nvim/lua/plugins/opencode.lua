return {
  "silvabyte/opencode.nvim",
  dependencies = { "nvim-lua/plenary.nvim" },
  -- Use "VeryLazy" if you want voice commands available immediately
  -- Use "InsertEnter" if you only need completions
  event = "VeryLazy",
  -- Options
  opts = {
    completion = {
      auto_trigger = true, -- complete as you type
      debounce = 150, -- ms to wait
      accept_key = "<Tab>",
      dismiss_key = "<C-e>",
      --etc
    },
    model = {
      provider = "zen-coding-plan",
      model_id = "glm-4.6",
      -- or big pickle, big pickle, big pickle!
      -- provider = "opencode",
      -- model_id = "big-pickle"
    },
  },
}
