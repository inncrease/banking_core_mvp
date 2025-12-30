# user service requirements

## Data Model Description: User

The table below describes the attributes for the User entity.

| Attribute | Data Type | Mandatory | Unique | Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | UUID (Text) | Yes | Yes (PK) | Unique identifier for the record. |
| `first_name` | String (50) | Yes | No | User's first name. |
| `last_name` | String (50) | Yes | No | User's last name. |
| `phone_number`| String (20) | Yes | Yes | Phone number in E.164 format. |
| `email` | String (100)| Yes | Yes | Email address (used as login). |
| `balance` | Decimal | No | No | User's balance. Default: 0.00 |
| `role` | String | Yes | No | Role: `user` or `admin`. Default: `user` |
| `created_at` | DateTime | Yes | No | Registration timestamp. |