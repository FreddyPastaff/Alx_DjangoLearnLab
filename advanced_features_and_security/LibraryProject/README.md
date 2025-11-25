Introduction to Django Development Environment Setup
# Permissions Setup

- Model: Document
- Custom Permissions:
  - can_view
  - can_create
  - can_edit
  - can_delete

- Groups:
  - Editors: can_edit, can_create
  - Viewers: can_view
  - Admins: all permissions

- Views:
  - Protected with @permission_required
