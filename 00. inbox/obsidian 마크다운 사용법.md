// M1 칩인 경우
export PATH=/opt/homebrew/bin:$PATH

// M1 칩이 아닌 경우
export PATH=/usr/local/bin:/usr/local/sbin:$PATH

// vi로 안들어가고 그냥 Terminal 창에서
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc