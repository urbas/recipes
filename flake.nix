{
  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.nixpkgs.url = "nixpkgs/nixos-unstable";

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      ...
    }:
    flake-utils.lib.eachSystem [ "x86_64-linux" "aarch64-linux" ] (
      system:
      with nixpkgs.legacyPackages.${system};
      let
        pkg = stdenvNoCC.mkDerivation {
          pname = "recipes";
          version = "0.0.0";
          src = self;
          nativeBuildInputs = [ pyDevEnv ];
          buildPhase = ''
            mkdocs build
          '';
          installPhase = ''
            mkdir -p $out
            cp -r site/* $out/
          '';
        };

        pyDevEnv = python3.withPackages (
          ps: with ps; [
            mkdocs
            mkdocs-mermaid2-plugin
          ]
        );

      in
      {
        packages.default = pkg;
        devShells.default = mkShell {
          packages = [
            nixfmt-rfc-style
            nodePackages.prettier
            prek
            treefmt
          ];
          inputsFrom = [
            pkg
          ];
        };
      }
    );
}
