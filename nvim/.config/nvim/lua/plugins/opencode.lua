return {
  {
    "nickjvandyke/opencode.nvim",
    version = "*", -- Latest stable release
    config = function()
    ---@type opencode.Opts
    vim.g.opencode_opts = {
      -- Your configuration, if any; goto definition on the type or field for details
    }

    vim.o.autoread = true -- Required for `opts.events.reload`
    local opencode = require("opencode")

    -- Recommended/example keymaps
    vim.keymap.set({ "n", "x" }, "<leader>oa", function()
      opencode.ask("@this: ")
    end, { desc = "Ask OpenCode…" })
    vim.keymap.set({ "n", "x" }, "<leader>os", function()
      opencode.select()
    end, { desc = "Select OpenCode…" })

    vim.keymap.set({ "n", "x" }, "go", function()
      return opencode.operator("@this ")
    end, { desc = "Append range to OpenCode", expr = true })
    vim.keymap.set("n", "goo", function()
      return opencode.operator("@this ") .. "_"
    end, { desc = "Append line to OpenCode", expr = true })
    vim.keymap.set("n", "ot", function()
      local buf ---@type integer?
      for _, b in ipairs(vim.api.nvim_list_bufs()) do
        if vim.bo[b].buftype == "terminal" and vim.api.nvim_buf_get_name(b):find("opencode", 1, true) then
          buf = b
          break
        end
      end
      if not buf then
        opencode.start()
        return
      end
      for _, w in ipairs(vim.api.nvim_list_wins()) do
        if vim.api.nvim_win_is_valid(w) and vim.api.nvim_win_get_buf(w) == buf then
          vim.api.nvim_win_hide(w)
          return
        end
      end
      vim.cmd("vertical sbuffer " .. buf)
      vim.cmd("wincmd p")
    end, { desc = "Toggle OpenCode window" })

    vim.keymap.set("n", "<S-C-u>", function()
      opencode.command("session.half.page.up")
    end, { desc = "Scroll OpenCode up" })
    vim.keymap.set("n", "<S-C-d>", function()
      opencode.command("session.half.page.down")
    end, { desc = "Scroll OpenCode down" })
    require("lualine").setup({
      sections = {
        lualine_z = {
          {
            opencode.statusline,
          },
        },
      },
    })
  end,
  },
  -- Extend LazyVim's built-in snacks.nvim with the opencode picker action.
  -- We must NOT call `require("snacks").setup()` here because LazyVim has
  -- already set it up; doing so triggers the "snacks.nvim is already setup"
  -- warning on startup. Using `opts` lets lazy.nvim deep-merge these values.
  {
    "folke/snacks.nvim",
    opts = {
      input = {
        enabled = true, -- Enhances `ask()`
      },
      picker = {
        enabled = true, -- Enhances `select()`
        actions = {
          ---@param picker snacks.Picker
          opencode_send = function(picker)
            local opencode = require("opencode")
            local items = vim.tbl_map(function(item) ---@param item snacks.picker.Item
              return item.file and opencode.format({ path = item.file, from = item.pos, to = item.end_pos })
                or item.text
            end, picker:selected({ fallback = true }))

            opencode.prompt(table.concat(items, ", ") .. " ")
          end,
        },
        win = {
          input = {
            keys = {
              ["<a-a>"] = { "opencode_send", mode = { "n", "i" } },
            },
          },
        },
      },
    },
  },
}
