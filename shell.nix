{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.poetry
    pkgs.python310
  ];

  shellHook = ''
    export PYTHONPATH=$(pwd)/src:$(pwd)/src/apps:$PYTHONPATH
    export DJANGO_SETTINGS_MODULE=shop.settings
    set -o allexport
    source .env
    set +o allexport
  '';
}
