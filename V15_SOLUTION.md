# FRAPPE V15 SOLUTION - Critical Missing Configuration

## Root Cause Found
Frappe v15.58.1 **requires `pyproject.toml`** with specific configuration that was missing from your app. This is a breaking change from earlier versions.

## Key V15 Requirements Applied

### 1. Updated pyproject.toml
- Added `[tool.bench.frappe-dependencies]` section
- Specified Frappe v15 compatibility: `frappe = ">=15.0.0,<16.0.0"`
- Used `flit_core` build backend (required for v15)
- Added proper project metadata structure

### 2. V15-Specific Changes
- **Minimum Node.js v18** required (check your server)
- **setup.py removed** - only pyproject.toml used
- **New build system** with stricter requirements

## Installation Commands for V15

```bash
# Method 1: Direct installation (recommended for v15)
cd /home/frappe/frappe-bench/apps
git clone [your-repo-url] easygo_education
echo "easygo_education" >> /home/frappe/frappe-bench/sites/apps.txt
bench --site [your-site] install-app easygo_education
bench build --app easygo_education
```

## If Still Failing - Check Server Requirements

```bash
# Check Node.js version (must be v18+)
node --version

# Update Node.js if needed
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Update bench to latest version
pip install --upgrade frappe-bench
```

## V15 Migration Notes
- Your app structure now matches v15 standards
- pyproject.toml properly configured for Frappe v15.58.1
- All deprecated v14 configurations removed

The build error should now be resolved with the proper v15 configuration.
