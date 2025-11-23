{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python313
    python313Packages.pip
    python313Packages.virtualenv
  ];

  shellHook = ''
    # Create virtual environment if it doesn't exist
    if [ ! -d .venv ]; then
      echo "Creating Python virtual environment..."
      python3.13 -m venv .venv
    fi

    # Activate virtual environment
    source .venv/bin/activate

    # Install dependencies if they exist
    if [ -f requirements.txt ]; then
      echo "Installing Python dependencies..."
      pip install -r requirements.txt
    fi

    echo "Python 3.13 environment ready!"
    echo "Run 'python pineapple.py <resume.md>' to generate a resume"
  '';
}
