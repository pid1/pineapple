{ pkgs, lib, config, inputs, ... }:

{
  # Python 3.14 environment
  languages.python = {
    enable = true;
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
