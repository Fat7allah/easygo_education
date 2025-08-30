# Frappe Build Error Fix Instructions

## Problem
The error `TypeError [ERR_INVALID_ARG_TYPE]: The "paths[0]" argument must be of type string. Received undefined` occurs during `bench get-app` when Frappe's esbuild system cannot resolve app paths.

## Root Cause Analysis
After analyzing ERPNext's structure, the issue is caused by:
1. **Incorrect build configuration files** - ERPNext doesn't use `build.json` in public folder
2. **Path resolution issues** in Frappe's esbuild system
3. **App structure mismatch** with Frappe's expectations

## Fixed App Structure (Now Matches ERPNext)
✅ **Corrected Files:**
- `package.json` - Simple structure like ERPNext (moved to root)
- Removed `public/build.json` - Not used by ERPNext
- Removed `public/js/index.js` - Unnecessary entry point
- Removed `.frapperc.js` - Not needed
- Reset `hooks.py` - Commented out asset includes

## Solution Methods (Try in Order)

### Method 1: Manual Installation (Recommended)
```bash
# Navigate to bench apps directory
cd /home/frappe/frappe-bench/apps

# Clone your app directly
git clone [your-repo-url] easygo_education

# Add to apps.txt
echo "easygo_education" >> /home/frappe/frappe-bench/sites/apps.txt

# Install the app to a site
bench --site [your-site] install-app easygo_education

# Build assets if needed
bench build --app easygo_education
```

### Method 2: Use Local Path Installation
```bash
# Install from local path
bench get-app /path/to/your/easygo_education

# Or if you're in the app directory
bench get-app .
```

### Method 3: Alternative Build Approach
```bash
# Try building without the problematic app first
bench build

# Then specifically build your app
bench build --app easygo_education
```

### Method 4: Skip Build During Installation
```bash
# Some versions support this flag
bench get-app [repo-url] --no-deps

# Or try installing to site without building
bench --site [site] install-app easygo_education --force
```

## If All Methods Fail
The issue might be with your Frappe/Bench version. Try:
```bash
# Update bench and frappe
bench update --reset

# Or check Frappe version compatibility
bench version
```

## App Structure Now Matches ERPNext Standards
Your app structure has been cleaned up to match ERPNext's minimal approach, which should resolve the build path resolution issues.
