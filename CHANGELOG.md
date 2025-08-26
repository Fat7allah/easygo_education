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
- Portal infrastructure with Student, Parent, and Teacher portals:
  - Student portal with dashboard, homework submissions, and grade viewing
  - Parent portal with children monitoring, meeting requests, and attendance justification
  - Teacher portal with attendance marking, assignment creation, and messaging
- Extended portal API endpoints for bulk operations and data retrieval
- Web forms for key processes:
  - Student enrollment form with bilingual support and dynamic validation
  - Meeting request form with teacher-student relationship validation
  - Homework submission form with file upload and draft saving
- Meeting Request doctype with approval workflow and notification system
- Print formats for professional document generation:
  - Student report card with academic performance and attendance summary
  - Fee invoice with payment instructions and multiple payment methods
- Bilingual interface support with language toggle functionality
- RTL (Right-to-Left) layout support for Arabic content
- Additional essential DocTypes for comprehensive education management:
  - Course Schedule doctype with timetable management and conflict detection
  - Exam doctype with scheduling, notifications, and results summary
  - Communication Log doctype for tracking all system communications
- Comprehensive script reports and dashboards for analytics:
  - Student Performance Report with grade distribution and performance metrics
  - Attendance Summary Report with attendance rates and status tracking
  - Fee Collection Report with payment analytics and collection rates
  - Education Manager Dashboard with enrollment trends and financial overview
  - Teacher Dashboard with class management and student performance tracking
  - Custom dashboard API methods for real-time metrics and analytics
