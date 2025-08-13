# EasyGo Education

A comprehensive, standalone Frappe application for educational institution management in Morocco, supporting French and Arabic languages with RTL layout.

## Features

- **Scolarité**: Student management, academics, timetables, assessments, homework system
- **Vie Scolaire**: Attendance, discipline, health records, extracurricular activities
- **Finances & RH**: Fee management, payroll, budgeting (ERP-lite + HR-lite)
- **Administration & Communication**: Messaging, notifications, parent-teacher meetings
- **Gestion Établissement**: Asset management, maintenance, transport, canteen
- **Référentiels**: Settings, grading scales, reference data
- **Student/Parent/Teacher Portals**: Role-based web interfaces
- **Bilingual Support**: French and Arabic with RTL layout
- **MASSAR Integration**: Export capabilities for Moroccan education system

## Requirements

- Python 3.11+
- Frappe Framework v15.x
- MariaDB
- Redis
- Node.js & npm

## Installation

### Local Development

```bash
# Initialize Frappe bench
bench init frappe-bench --frappe-branch version-15
cd frappe-bench

# Create new site
bench new-site easygo.local

# Get the app
bench get-app /path/to/easygo_education

# Install the app
bench --site easygo.local install-app easygo_education

# Migrate and build
bench --site easygo.local migrate
bench --site easygo.local build

# Start development server
bench start
```

### Remote Server Deployment

```bash
# On remote server
ssh user@remote
sudo apt update
sudo apt install -y python3.11 python3.11-venv mariadb-server redis-server nodejs npm

# Setup Frappe
bench init frappe-bench --frappe-branch version-15
cd frappe-bench

# Create site and install app
bench new-site easygo.remote
bench get-app https://github.com/USERNAME/easygo_education.git
bench --site easygo.remote install-app easygo_education
bench --site easygo.remote migrate && bench --site easygo.remote build

# Start production
bench start

# Run tests
bench --site easygo.remote run-tests --app easygo_education
```

## Working in Other IDEs

This project is designed to work seamlessly across different development environments:

### VS Code
1. Install Python extension
2. Open project folder
3. Configure Python interpreter: `Ctrl+Shift+P` → "Python: Select Interpreter"
4. Install recommended extensions from `.vscode/extensions.json`

### PyCharm/JetBrains IDEs
1. Open project as Python project
2. Configure Python interpreter in Settings → Project → Python Interpreter
3. Enable EditorConfig support in Settings → Editor → Code Style
4. Configure code style to use Black formatter

### Vim/Neovim
1. Install Python LSP server: `pip install python-lsp-server`
2. Configure your editor to use `.editorconfig`
3. Add Black and Ruff integration to your config
4. Use vim-frappe plugin for Frappe-specific syntax highlighting

### Remote Development (SSH)
1. **VS Code Remote-SSH**: Install Remote-SSH extension, connect to server
2. **PyCharm Professional**: Use SSH interpreter configuration
3. **Terminal-based**: Use tmux/screen for persistent sessions

## Portal Routes

### Student Portal (`/student`)
- Dashboard, timetable, attendance history
- Homework submissions, grades, report cards
- Activities registration, transport info
- Class messaging with teachers

### Parent Portal (`/parent`)
- Children overview with alerts
- Fee bills and payment (stub integration)
- Attendance justifications, consent forms
- Parent-teacher meeting booking
- Secure messaging with teachers

### Teacher Portal (`/teacher`)
- Class management, lesson plans
- Attendance marking, homework assignment
- Assessment creation and grading
- Report card generation
- Class communication and meeting confirmations

## Sample Logins (After Seed Data)

- **Administrator**: admin@easygo.local / admin
- **Teacher**: teacher@easygo.local / teacher123
- **Parent**: parent@easygo.local / parent123
- **Student**: student@easygo.local / student123

## Development Commands

```bash
# Format code
make format

# Run linting
make lint

# Run tests
make test

# Start development server
make bench-start

# Build assets
make build
```

## Testing

Run the complete test suite:

```bash
bench --site easygo.local run-tests --app easygo_education
```

## License

MIT License

## Support

For support and questions, please open an issue on GitHub.
