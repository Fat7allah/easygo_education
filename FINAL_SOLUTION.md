# FINAL SOLUTION - Bypass bench get-app Completely

The `bench get-app` command has a persistent bug in Frappe's esbuild system. Here's how to install your app manually:

## Step 1: Manual Installation (Server Side)

```bash
# SSH into your server and navigate to bench directory
cd /home/frappe/frappe-bench/apps

# Clone your app directly (replace with your actual repo URL)
git clone https://github.com/yourusername/easygo_education.git easygo_education

# Add the app to apps.txt
echo "easygo_education" >> /home/frappe/frappe-bench/sites/apps.txt

# Install the app to your site (replace 'yoursite' with actual site name)
bench --site yoursite install-app easygo_education

# Build assets (this should work now that the app is properly installed)
bench build
```

## Step 2: Alternative if Git Clone Fails

```bash
# Upload your app folder directly to the server
# Use SCP, SFTP, or your hosting provider's file manager
# Copy the entire easygo_education folder to /home/frappe/frappe-bench/apps/

# Then continue with:
echo "easygo_education" >> /home/frappe/frappe-bench/sites/apps.txt
bench --site yoursite install-app easygo_education
bench build
```

## Step 3: If Build Still Fails

```bash
# Try building without your app first
bench build --apps frappe

# Then build just your app
bench build --app easygo_education

# Or skip building entirely and copy assets manually
mkdir -p /home/frappe/frappe-bench/sites/assets/easygo_education
cp -r /home/frappe/frappe-bench/apps/easygo_education/easygo_education/public/* /home/frappe/frappe-bench/sites/assets/easygo_education/
```

## Why This Works

- Bypasses the problematic `bench get-app` command entirely
- Manually adds the app to the bench ecosystem
- Installs the app directly to the site
- Builds assets after proper installation

## Root Cause

The `bench get-app` command triggers Frappe's esbuild system before the app is properly integrated into the bench, causing path resolution failures. Manual installation ensures the app is properly registered before any build processes run.

Try Step 1 first - this should resolve your installation issue completely.
