# Backend System Modifications Summary

## Overview
This document summarizes all modifications made to the ZO LITS backend system to enforce email domain validation, username format validation, field uniqueness, and auto-stamping of resolved issues.

---

## 1. Email Validation

### Requirement
Emails entered by users must contain the domain @zetdc.co.zw

### Implementation
- **File**: [core/serializers.py](core/serializers.py#L32-L37)
- **Method**: `UserRegistrationSerializer.validate_email()`
- **Validation Rules**:
  - Email must end with `@zetdc.co.zw`
  - Email must be unique in the system
  - Duplicate emails are rejected with error: "A user with this email already exists."

### Code Snippet
```python
def validate_email(self, value):
    if not value.endswith("@zetdc.co.zw"):
        raise serializers.ValidationError("Email must belong to the @zetdc.co.zw domain.")
    if User.objects.filter(email=value).exists():
        raise serializers.ValidationError("A user with this email already exists.")
    return value
```

---

## 2. Username Validation

### Requirement
Usernames should start with "ze" followed by a variable number of digits

### Implementation
- **File**: [core/serializers.py](core/serializers.py#L39-L42)
- **Method**: `UserRegistrationSerializer.validate_username()`
- **Validation Rules**:
  - Username must match the regex pattern `^ze\d+$` (starts with "ze", followed by one or more digits)
  - Username must be unique in the system (enforced by Django User model)
  - Examples of valid usernames: `ze123`, `ze456789`, `ze1`

### Code Snippet
```python
def validate_username(self, value):
    if not re.match(r'^ze\d+$', value):
        raise serializers.ValidationError("Username must start with 'ze' followed by digits.")
    if User.objects.filter(username=value).exists():
        raise serializers.ValidationError("A user with this username already exists.")
    return value
```

---

## 3. Email and Username Uniqueness

### Implementation Details
- **Email Uniqueness**: Enforced in `UserRegistrationSerializer.validate_email()`
- **Username Uniqueness**: 
  - Django's User model enforces this automatically
  - Additional validation added in `UserRegistrationSerializer.validate_username()`

---

## 4. New "resolved_by" Column in Issues Table

### Requirement
Add a "resolved_by" column that auto-stamps when the resolved status is selected

### Implementation
- **Database Field**: New ForeignKey field `resolved_by` in the Issue model
  - Points to the User model (WHO resolved the issue)
  - Nullable, set to NULL when issue is not resolved
  - Related name: `issues_resolved_by_user`

- **File**: [core/models.py](core/models.py#L97-L105)
- **Field Definition**:
```python
resolved_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='issues_resolved_by_user',
)
```

### Auto-Stamping Logic
- **File**: [core/serializers.py](core/serializers.py#L200-L230)
- **Method**: `IssueSerializer.update()`
- **Behavior**:
  - When an issue's status is changed to a resolved state:
    - `resolved_by` is automatically set to the currently authenticated user
    - `date_issue_resolved` is automatically set to the current timestamp
  - When an issue is moved OUT of a resolved state:
    - `resolved_by` is cleared to NULL
    - `date_issue_resolved` is cleared to NULL

### Database Migration
- **Migration File**: `core/migrations/0004_issue_resolved_by.py`
- **Status**: Successfully applied
- **Changes**: Adds the `resolved_by` ForeignKey column to the `core_issue` table

---

## 5. Region-Depot Validation

### Requirement
Ensure frontend data sends valid depot selections that match the selected region

### Implementation
- **File**: [core/serializers.py](core/serializers.py#L155-L159)
- **Method**: `IssueSerializer.validate()`
- **Validation Logic**:
  - When both `region` and `depot` are provided in a request
  - The system validates that `depot.region == region`
  - If the depot does NOT belong to the selected region, validation fails with error:
    ```
    "Depot 'XXX' does not belong to region 'YYY'."
    ```

### Code Snippet
```python
def validate(self, data):
    region = data.get("region")
    depot = data.get("depot")
    if region and depot and depot.region != region:
        raise serializers.ValidationError({"depot": f"Depot '{depot.name}' does not belong to region '{region.name}'."})
    return data
```

---

## Modified Files

1. **[core/models.py](core/models.py)**
   - Added `resolved_by` ForeignKey field to the Issue model (lines 97-105)

2. **[core/serializers.py](core/serializers.py)**
   - Enhanced `UserRegistrationSerializer.validate_email()` - Added uniqueness check
   - Enhanced `UserRegistrationSerializer.validate_username()` - Added format and uniqueness validation
   - Added `resolved_by` to IssueSerializer fields and read_only_fields
   - Updated `IssueSerializer.update()` method to auto-stamp `resolved_by` when status changes to resolved

3. **[core/migrations/0004_issue_resolved_by.py](core/migrations/0004_issue_resolved_by.py)**
   - New migration file that adds the `resolved_by` column to the Issue table

---

## Validation Summary

| Feature | Validation Type | Status | Location |
|---------|-----------------|--------|----------|
| Email Domain | @zetdc.co.zw | ✓ Implemented | UserRegistrationSerializer |
| Email Uniqueness | Duplicate check | ✓ Implemented | UserRegistrationSerializer |
| Username Format | ze + digits | ✓ Implemented | UserRegistrationSerializer |
| Username Uniqueness | Duplicate check | ✓ Implemented | UserRegistrationSerializer |
| resolved_by Auto-stamp | On status resolution | ✓ Implemented | IssueSerializer.update() |
| Region-Depot Match | Depot ⊂ Region | ✓ Implemented | IssueSerializer.validate() |

---

## Testing the Implementation

### Test Email Validation
```bash
# This should FAIL - wrong domain
POST /api/auth/register/
{
  "username": "ze123",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "pass123",
  "confirm_password": "pass123"
}
# Response: 400 - "Email must belong to the @zetdc.co.zw domain."

# This should SUCCEED
POST /api/auth/register/
{
  "username": "ze456",
  "email": "user@zetdc.co.zw",
  "first_name": "John",
  "last_name": "Doe",
  "password": "pass123",
  "confirm_password": "pass123"
}
# Response: 201 - User created with token
```

### Test Username Validation
```bash
# This should FAIL - no digits
POST /api/auth/register/
{
  "username": "zeabc",
  "email": "user@zetdc.co.zw",
  ...
}
# Response: 400 - "Username must start with 'ze' followed by digits."

# This should FAIL - doesn't start with 'ze'
POST /api/auth/register/
{
  "username": "ab123",
  "email": "user@zetdc.co.zw",
  ...
}
# Response: 400 - "Username must start with 'ze' followed by digits."
```

### Test Issue Resolution Auto-Stamping
```bash
# Update an issue to resolved status
PATCH /api/issues/{id}/
{
  "status": 5  # ID of resolved status
}

# The response will include:
{
  "resolved_by": {user_id},
  "date_issue_resolved": "2026-03-14T10:30:00Z"
}
```

### Test Region-Depot Validation
```bash
# This should FAIL - depot from different region
POST /api/issues/
{
  "region": 1,        # Southern region
  "depot": 5,         # Northern depot
  ...
}
# Response: 400 - "Depot 'XXX' does not belong to region 'Southern'."

# This should SUCCEED
POST /api/issues/
{
  "region": 1,
  "depot": 2,  # Depot that belongs to region 1
  ...
}
# Response: 201 - Issue created
```

---

## Notes

- All validations are enforced at the serializer level, rejecting invalid data before it reaches the database
- The auto-stamping of `resolved_by` preserves the user who actually changed the status
- If an issue is marked as resolved by an unauthenticated user, the system will attempt to use the first user in the system as a fallback (for backward compatibility)
- The `issue_resolved_by` field remains for backward compatibility alongside the new `resolved_by` field

---

## Next Steps

1. Test the API endpoints with various inputs to confirm validations work correctly
2. Update frontend accordingly to:
   - Enforce email domain validation on the client side
   - Enforce username format (ze + digits) on the client side
   - Ensure depot options are filtered based on selected region
3. Monitor logs to catch any validation errors from frontend requests
