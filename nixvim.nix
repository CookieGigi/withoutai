# Project-specific nixvim overrides for without-ai (Python/FastAPI)
{pkgs, ...}: {
  plugins = {
    # LSP servers
    lsp.servers = {
      pyright = {
        enable = true;
        package = pkgs.pyright;
      };
    };

    # Formatting (match ruff-format pre-commit hook)
    conform-nvim.settings.formatters_by_ft = {
      python = ["ruff_format"];
    };

    # Linting (match ruff and mypy pre-commit hooks)
    lint.lintersByFt = {
      python = [
        "ruff"
        "mypy"
      ];
    };
  };
}
