# Frappe Build Error Fix Instructions

## Problem
The error `TypeError [ERR_INVALID_ARG_TYPE]: The "paths[0]" argument must be of type string. Received undefined` occurs during `bench get-app` when Frappe's esbuild system cannot resolve app paths.

## Solution Options

### Option 1: Skip Assets During Installation (Recommended)
```bash
# Install the app without building assets
bench get-app --skip-assets easygo_education

# Then build assets manually after installation
bench build --app easygo_education
```

### Option 2: Use Alternative Installation Method
```bash
# Clone the app manually to the apps directory
cd /home/frappe/frappe-bench/apps
git clone [your-repo-url] easygo_education

# Add to apps.txt
echo "easygo_education" >> /home/frappe/frappe-bench/sites/apps.txt

# Install without assets
bench --site [your-site] install-app easygo_education --skip-assets

# Build assets separately
bench build --app easygo_education
```

### Option 3: If Still Failing - Manual Asset Copy
```bash
# Copy assets to the sites directory manually
mkdir -p /home/frappe/frappe-bench/sites/assets/easygo_education
cp -r /home/frappe/frappe-bench/apps/easygo_education/easygo_education/public/* /home/frappe/frappe-bench/sites/assets/easygo_education/
```

## Files Created to Fix Build Configuration
1. `package.json` - App build configuration
2. `public/build.json` - Asset mapping configuration  
3. `public/js/index.js` - Entry point for module system
4. `.frapperc.js` - Frappe configuration
5. Updated `hooks.py` - Asset inclusion paths

## Root Cause
This error typically occurs due to:
- Missing build configuration files
- Path resolution issues in Frappe's esbuild system
- Symlink handling problems in newer Frappe versions
