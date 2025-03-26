{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python313;
        # python = pkgs.python3;
        # pythonEnv = python.withPackages (p: [
        #   # Here goes all the libraries that can't be managed by uv because of dynamic linking issues
        #   # or that you just want to be managed by nix for one reason or another
        #   p.pandas
        # ]);
      in
      {
        devShells.default =
          with pkgs;
          mkShell {
            packages = [
              uv
              python
              # pythonEnv
            ];

            shellHook = ''
              exec fish
            '';

            env.UV_PYTHON = "${python}";
            env.UV_PYTHON_PREFERENCE = "only-system";
          };
      }
    );
}
