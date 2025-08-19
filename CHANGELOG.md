# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-08-19

### Added
- Initial project structure with CHANGELOG.md
- .editorconfig for consistent code formatting across IDEs
- CONTRIBUTING.md with Conventional Commits guidelines
- README section for cross-IDE compatibility (VS Code, PyCharm, Vim, Remote-SSH)
- Foundation for standalone Frappe app with 7 modules
- Bilingual support (FR/AR) with RTL layout for Arabic
- Student/Parent/Teacher portal architecture
- Complete modular repository scaffold with all directories and core files
- School Settings and Finance Settings doctype foundations
- Print format templates for report cards and fee bills with RTL support
- Translation files for French and Arabic
- CSS and JavaScript foundations for portal functionality
- Hooks configuration with document events and scheduled tasks
- Bootstrap patch framework for demo data
- Core DocTypes implementation with business rules:
  - Student doctype with MASSAR validation and user account creation
  - Academic Year doctype with date validation and default year management
  - Fee Bill doctype with FIFO payment allocation and ledger integration
  - Student Attendance doctype with guardian notifications and justification workflow
  - School Class doctype with capacity management and subject assignment
  - Subject doctype with scoring configuration and level categorization
  - Homework doctype with automated notifications and submission tracking
  - Homework Submission doctype with late detection and grading workflow
  - Grade doctype with percentage calculation and letter grade assignment
  - Employee doctype with user account creation and role assignment
  - Assessment doctype with scheduling and grading summary analytics
- Document event hooks for validation and automated actions
- Scheduled job system for daily, weekly, and monthly operations
- Role-based permissions and portal access control
- Comprehensive business rule validation across all DocTypes
- Automated notification system for students, parents, and teachers
