-- Prefer ruff-lsp to Pyright for linting and analysis
-- local lspconfig = require("lspconfig")
-- local on_attach = function(client, bufnr)
--   -- Disable hover in favor of Pyright
--   client.server_capabilities.hoverProvider = false
-- end
-- lspconfig.ruff_lsp.setup({
--   on_attach = on_attach,
--   init_options = {
--     settings = {
--       -- Any extra CLI arguments for `ruff` go here.
--       args = {},
--     },
--   },
-- })
-- lspconfig.pyright.setup({
--   settings = {
--     pyright = {
--       disableOrganizeImports = true, -- Using Ruff
--     },
--     python = {
--       analysis = {
--         ignore = { "*" }, -- Using Ruff
--       },
--     },
--   },
-- })
require("lspconfig").ruff.setup({
  init_options = {
    settings = {
      -- Ruff language server settings go here
    },
  },
})
vim.lsp.enable("ty")
