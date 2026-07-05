#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$HOME/Documents/manager-hub"
VENV_DIR="$PROJECT_DIR/venv"
PYTHON_VERSION="3.13"
BREW_PACKAGES=(python@3.13 node tesseract gh rclone)

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()  { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
err()  { echo -e "${RED}[✗]${NC} $1"; }

echo "=============================="
echo "  Manager Hub — Bootstrap"
echo "=============================="
echo ""

# ──────────────────────────────────────────────
# 1. Xcode Command Line Tools
# ──────────────────────────────────────────────
echo "--- Step 1: Xcode Command Line Tools ---"
if xcode-select -p &>/dev/null; then
    log "Xcode CLT already installed"
else
    warn "Installing Xcode Command Line Tools..."
    xcode-select --install || true
    echo "  Press any key after installation completes..."
    read -r -n 1
    if ! xcode-select -p &>/dev/null; then
        err "Xcode CLT installation failed. Please install manually and re-run."
        exit 1
    fi
    log "Xcode CLT installed"
fi

# ──────────────────────────────────────────────
# 2. Homebrew
# ──────────────────────────────────────────────
echo ""
echo "--- Step 2: Homebrew ---"
if command -v brew &>/dev/null; then
    log "Homebrew already installed ($(brew --version | head -1))"
else
    warn "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> "$HOME/.zprofile"
    eval "$(/opt/homebrew/bin/brew shellenv)"
    log "Homebrew installed"
fi

# ──────────────────────────────────────────────
# 3. Homebrew Packages
# ──────────────────────────────────────────────
echo ""
echo "--- Step 3: Homebrew Packages ---"
for pkg in "${BREW_PACKAGES[@]}"; do
    if brew list "$pkg" &>/dev/null 2>&1; then
        log "$pkg already installed"
    else
        warn "Installing $pkg..."
        brew install "$pkg"
        log "$pkg installed"
    fi
done

# ──────────────────────────────────────────────
# 4. LibreOffice Symlink
# ──────────────────────────────────────────────
echo ""
echo "--- Step 4: LibreOffice CLI Symlink ---"
LO_APP="/Applications/LibreOffice.app"
LO_BIN="$LO_APP/Contents/MacOS/soffice"
SYMLINK="/usr/local/bin/libreoffice"

if [ ! -d "$LO_APP" ]; then
    warn "LibreOffice.app not found at /Applications. Skipping symlink."
elif [ -L "$SYMLINK" ] && [ "$(readlink "$SYMLINK")" = "$LO_BIN" ]; then
    log "LibreOffice symlink already exists"
else
    if [ ! -d "/usr/local/bin" ]; then
        sudo mkdir -p "/usr/local/bin"
    fi
    sudo ln -sf "$LO_BIN" "$SYMLINK"
    log "Symlink created: $SYMLINK -> $LO_BIN"
fi

# ──────────────────────────────────────────────
# 5. Python Virtual Environment
# ──────────────────────────────────────────────
echo ""
echo "--- Step 5: Python Virtual Environment ---"
PYTHON_BIN="$(brew --prefix python@3.13)/bin/python3.13"

if [ ! -f "$PYTHON_BIN" ]; then
    err "Python $PYTHON_VERSION not found at $PYTHON_BIN"
    exit 1
fi

if [ -d "$VENV_DIR" ]; then
    log "Virtual environment already exists at $VENV_DIR"
else
    "$PYTHON_BIN" -m venv "$VENV_DIR"
    log "Virtual environment created at $VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
pip install --upgrade pip
log "pip upgraded"

# ──────────────────────────────────────────────
# 6. Install Python Packages
# ──────────────────────────────────────────────
echo ""
echo "--- Step 6: Python Packages ---"
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    pip install -r "$PROJECT_DIR/requirements.txt"
    log "Python packages installed from requirements.txt"
else
    warn "requirements.txt not found — run this script from the project directory"
fi

# ──────────────────────────────────────────────
# 7. Wrangler (Cloudflare)
# ──────────────────────────────────────────────
echo ""
echo "--- Step 7: Wrangler CLI ---"
if command -v wrangler &>/dev/null; then
    log "Wrangler already installed ($(wrangler --version 2>/dev/null || echo 'ok'))"
else
    warn "Installing wrangler via npm..."
    npm install -g wrangler
    log "Wrangler installed"
fi

# ──────────────────────────────────────────────
# 8. GitHub Setup
# ──────────────────────────────────────────────
echo ""
echo "--- Step 8: GitHub Setup ---"
if command -v gh &>/dev/null; then
    if gh auth status &>/dev/null; then
        log "GitHub CLI authenticated"
    else
        warn "Please authenticate with GitHub:"
        gh auth login --git-protocol https
    fi

    if [ ! -d "$PROJECT_DIR/.git" ]; then
        cd "$PROJECT_DIR"
        git init
        git add -A
        git commit -m "Initial scaffold — manager-hub backend infrastructure"
        gh repo create manager-hub --public --source=. --push --remote=origin
        log "GitHub repo created and pushed"
    else
        if git remote get-url origin &>/dev/null; then
            log "Git remote already configured"
        else
            warn "Git repo exists but no remote — creating..."
            gh repo create manager-hub --public --source=. --push --remote=origin
            log "GitHub repo created and pushed"
        fi
    fi
else
    warn "gh CLI not installed — skipping GitHub setup"
fi

# ──────────────────────────────────────────────
# 9. pre-commit Hooks
# ──────────────────────────────────────────────
echo ""
echo "--- Step 9: pre-commit Hooks ---"
if [ -f "$PROJECT_DIR/.pre-commit-config.yaml" ]; then
    cd "$PROJECT_DIR"
    if [ -d "$PROJECT_DIR/.git" ]; then
        pre-commit install
        log "pre-commit hooks installed"
    else
        warn "No git repo yet — pre-commit hooks deferred to after git init"
    fi
else
    warn ".pre-commit-config.yaml not found — skipping"
fi

# ──────────────────────────────────────────────
# 10. macOS LaunchAgent
# ──────────────────────────────────────────────
echo ""
echo "--- Step 10: LaunchAgent (Folder Watcher) ---"
PLIST_SRC="$PROJECT_DIR/LaunchAgents/com.managerhub.watcher.plist"
PLIST_DST="$HOME/Library/LaunchAgents/com.managerhub.watcher.plist"

if [ -f "$PLIST_SRC" ]; then
    mkdir -p "$HOME/Library/LaunchAgents"
    cp "$PLIST_SRC" "$PLIST_DST"
    launchctl load "$PLIST_DST" 2>/dev/null || true
    log "LaunchAgent installed and loaded"
else
    warn "LaunchAgent plist not found — skipping"
fi

# ──────────────────────────────────────────────
# Done
# ──────────────────────────────────────────────
echo ""
echo "=============================="
echo "  Manager Hub — Bootstrap Complete!"
echo "=============================="
echo ""
echo "  Project:  $PROJECT_DIR"
echo "  Venv:     $VENV_DIR"
echo ""
echo "  Activate: source $VENV_DIR/bin/activate"
echo "  Run app:  uvicorn app.main:app --reload"
echo "  Watcher:  launchctl start com.managerhub.watcher"
echo ""
