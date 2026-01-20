{ pkgs, lib, config, inputs, ... }:

{
  # Python 3.13 environment
  languages.python = {
    enable = true;
    package = pkgs.python313.withPackages (ps: [
      ps.markdown
      ps.reportlab
    ]);
  };

  enterShell = ''
    echo "Python 3.13 environment ready!"
    echo "Run 'python pineapple.py <resume.md>' to generate a resume"
  '';
}
