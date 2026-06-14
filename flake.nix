{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    git-hooks = {
      url = "github:cachix/git-hooks.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = {
    nixpkgs,
    flake-utils,
    git-hooks,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {inherit system;};

      pre-commit-check = git-hooks.lib.${system}.run {
        src = ./.;
        hooks = {
          alejandra.enable = true;
          deadnix = {
            enable = true;
            excludes = [".direnv"];
          };
          flake-checker.enable = true;
          ruff.enable = true;
          ruff-format.enable = true;
          mypy = {
            enable = true;
            args = ["--ignore-missing-imports"];
          };
          end-of-file-fixer.enable = true;
          trim-trailing-whitespace.enable = true;
          check-merge-conflicts.enable = true;
        };
      };
    in {
      checks.pre-commit-check = pre-commit-check;
      formatter = let
        inherit (pre-commit-check) config;
        inherit (config) package configFile;
      in
        pkgs.writeShellScriptBin "pre-commit-run" ''
          ${pkgs.lib.getExe package} run --all-files --config ${configFile}
        '';

      devShells.default = pkgs.mkShell {
        shellHook = ''
          # Guard against global core.hooksPath which breaks pre-commit hook installation.
          _global_hooksPath="$(${pkgs.git}/bin/git config --global core.hooksPath 2>/dev/null || true)"
          if [ -n "$_global_hooksPath" ]; then
            echo ""
            echo "WARNING: core.hooksPath is set globally ('$_global_hooksPath')."
            echo "This prevents pre-commit hooks from being installed by the Nix devShell."
            echo "Remove it with: git config --global --unset-all core.hooksPath"
            echo ""
          fi
          unset _global_hooksPath

          ${pre-commit-check.shellHook}

          export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH"
        '';
        buildInputs = with pkgs;
          [
            git
            python313
            uv
            gnumake
            ruff
            alejandra
            stdenv.cc.cc.lib
          ]
          ++ pre-commit-check.enabledPackages;
      };
    });
}
