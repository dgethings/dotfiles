return {
  {
    "carderne/pi-nvim",
    config = function()
      require("pi-nvim").setup({
        set_default_keymaps = false,
      })
      vim.keymap.set("n", "<leader>aa", ":Pi<CR>", { desc = "Send prompt to agent" })
      vim.keymap.set({ "n", "v" }, "<leader>as", ":PiSendSelection<cr>", { desc = "Send selection to Pi" })

      -- Send all diagnostics in the current buffer to the pi agent
      vim.keymap.set("n", "<leader>ad", function()
        local pi = require("pi-nvim")
        local file = vim.fn.expand("%:.")
        local diags = vim.diagnostic.get(0)

        if #diags == 0 then
          vim.notify("No diagnostics in buffer", vim.log.levels.INFO)
          return
        end

        table.sort(diags, function(a, b)
          if a.lnum ~= b.lnum then
            return a.lnum < b.lnum
          end
          return (a.col or 0) < (b.col or 0)
        end)

        local severity_name = {
          [vim.diagnostic.severity.ERROR] = "Error",
          [vim.diagnostic.severity.WARN] = "Warning",
          [vim.diagnostic.severity.INFO] = "Info",
          [vim.diagnostic.severity.HINT] = "Hint",
        }

        local lines = {}
        for _, d in ipairs(diags) do
          local sev = severity_name[d.severity] or "Unknown"
          local src = d.source and ("[" .. d.source .. "]") or ""
          local code = d.code and (" (" .. tostring(d.code) .. ")") or ""
          table.insert(
            lines,
            string.format(
              "L%d:%d  %s%s%s  %s",
              d.lnum + 1,
              d.col + 1,
              sev,
              code,
              src == "" and "" or (" " .. src),
              d.message
            )
          )
        end

        local message = string.format(
          "Here are all %d diagnostics reported in `%s`. " .. "Please help me fix them.\n\n" .. "```\n%s\n```",
          #diags,
          file,
          table.concat(lines, "\n")
        )
        pi.prompt(message)
        vim.notify(string.format("Sent %d diagnostics from %s to pi", #diags, file), vim.log.levels.INFO)
      end, { desc = "Send all diagnostics to pi" })
    end,
  },
}
