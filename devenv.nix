{ pkgs, lib, config, inputs, ... }:

{
  # Python 3.14 environment
  languages.python = {
    enable = true;
    # sadr: hold at python314, python315 meson-python 0.20.0 fails test_limited_api in nixpkgs 674a202, which blocks pillow
    package = pkgs.python314.withPackages (ps: [
      ps.markdown
      ps.reportlab
    ]);
  };

  enterShell = ''
    echo "Python 3.14 environment ready!"
    echo "Run 'python pineapple.py <resume.md>' to generate a resume"
  '';
}
