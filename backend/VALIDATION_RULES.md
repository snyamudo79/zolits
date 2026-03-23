# Backend Validation Rules - Quick Reference

## 1. User Registration Validation

### Email Validation
- **Rule**: Must end with `@zetdc.co.zw`
- **Rule**: Must be unique (no duplicates)
- **Error Response**: 
  ```json
  {
    "email": ["Email must belong to the @zetdc.co.zw domain."]
  }
  ```
  or
  ```json
  {
    "email": ["A user with this email already exists."]
  }
  ```

### Username Validation
- **Rule**: Must match pattern `ze` + digits (e.g., `ze123`, `ze456789`)
- **Rule**: Must be unique (no duplicates)
- **Error Response**:
  ```json
  {
    "username": ["Username must start with 'ze' followed by digits."]
  }
  ```
  or
  ```json
  {
    "username": ["A user with this username already exists."]
  }
  ```

### Example Valid Registration
```json
{
  "username": "ze12345",
  "email": "john.doe@zetdc.co.zw",
  "first_name": "John",
  "last_name": "Doe",
  "password": "securePassword123",
  "confirm_password": "securePassword123"
}
```

---

## 2. Issue Creation/Update Validation

### Region-Depot Validation
- **Rule**: The selected depot must belong to the selected region
- **Error Response**:
  ```json
  {
    "depot": ["Depot 'XXX (NN)' does not belong to region 'YYYY'."]
  }
  ```

### Example Valid Request
```json
{
  "region": 1,
  "depot": 2,
  "module": 1,
  "description": "USER CANNOT LOGIN WITH CORRECT CREDENTIALS",
  "raised_by_name": "John Smith",
  "contact_phone": "+263 712 345 678",
  "severity": 1
}
```

---

## 3. Issue Resolution (Auto-Stamping)

### Initial Status
- **Rule**: When an issue is created from the frontend, the `status` is automatically set to `PENDING`.
- **Note**: Users are not required to provide a `status` in the request body. If provided, it will be ignored.

### When Issue is Marked as Resolved
When an issue's status is changed to a resolved state:
- `resolved_by` field is automatically set to the current user
- `date_issue_resolved` is automatically set to current timestamp
- These fields are READ-ONLY and cannot be manually set by API

### Response Example
```json
{
  "id": 123,
  "issue_number": "SU32",
  "status": 5,
  "resolved_by": 42,
  "date_issue_resolved": "2026-03-14T10:30:00Z",
  ...
}
```

### When Issue is Moved Out of Resolved State
- `resolved_by` is automatically cleared to NULL
- `date_issue_resolved` is automatically cleared to NULL

---

## 4. Validation Error Handling

### Standard Error Response Format
```json
HTTP 400 Bad Request

{
  "field_name": ["Error message 1", "Error message 2"]
}
```

### Common Error Scenarios

#### Duplicate Email
```json
{
  "email": ["A user with this email already exists."]
}
```

#### Invalid Username Format
```json
{
  "username": ["Username must start with 'ze' followed by digits."]
}
```

#### Invalid Email Domain
```json
{
  "email": ["Email must belong to the @zetdc.co.zw domain."]
}
```

#### Depot from Wrong Region
```json
{
  "depot": ["Depot 'Harare North (NU)' does not belong to region 'Southern'."]
}
```

---

## 5. Backend Endpoints Summary

### Authentication
- `POST /api/auth/register/` - Register new user (email/username validation)
- `POST /api/auth/login/` - Login user

### Issues
- `POST /api/issues/` - Create issue (region-depot validation)
- `PATCH /api/issues/{id}/` - Update issue (auto-stamp on resolution)
- `GET /api/issues/` - List all issues

### Supporting Data
- `GET /api/regions/` - List all regions
- `GET /api/depots/` - List all depots (includes associated region)
- `GET /api/modules/` - List all modules
- `GET /api/issue-statuses/` - List all status options
- `GET /api/issue-severities/` - List all severity levels

---

## 6. Database Fields Reference

### Issue Model - New Fields
- `resolved_by` (ForeignKey to User)
  - Nullable
  - Auto-populated when status → resolved
  - Auto-cleared when status ← resolved
  - Related name: `issues_resolved_by_user`

### User Model - Existing Fields Used for Validation
- `username` - Must be unique and follow `ze\d+` pattern
- `email` - Must be unique and end with `@zetdc.co.zw`

---

## 7. Testing Checklist

- [ ] Invalid email domain rejected
- [ ] Duplicate email rejected
- [ ] Invalid username format rejected  
- [ ] Duplicate username rejected
- [ ] Issue with depot from wrong region rejected
- [ ] resolv_by auto-populated on resolution
- [ ] resolved_by cleared on unresolving
- [ ] All validation errors return 400 Bad Request

---

## Notes for Frontend Development

1. **Email Input**: Add client-side validation for `@zetdc.co.zw` domain
2. **Username Input**: Add client-side validation for pattern `ze` + digits
3. **Depot Selection**: Filter available depots based on selected region
4. **Display resolved_by**: Show the user who resolved the issue
5. **Error Handling**: Parse and display validation errors to users

All validations are enforced server-side, but client-side validation improves user experience.
