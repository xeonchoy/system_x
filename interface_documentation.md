# System X Interface Documentation

## API Endpoints Table

| 模块名称 | 小件名称 | 接口名称 | 描述 |
|----------|----------|----------|------|
| 认证模块 | 注册组件 | /register | 用户注册接口 |
| 认证模块 | 登录组件 | /login | 用户登录接口 |
| 消息模块 | 同步组件 | /sync | 消息同步接口 |

## Detailed Documentation

### Authentication Module
- `/register` (POST): Register new user
- `/login` (POST): Authenticate user

### Messaging Module
- `/sync` (POST): Start message synchronization
  - Requires authentication
  - Returns JSON response with sync status
  - Example success response:
    ```json
    {
      "status": "success", 
      "message": "Sync started successfully"
    }
    ```
  - Example error response:
    ```json
    {
      "status": "error",
      "message": "Error description",
      "code": 500
    }
    ```

## Database Schema
- users table:
  - id (INTEGER PRIMARY KEY)
  - username (TEXT UNIQUE)
  - password (TEXT)

## API Responses
- Success: {"status": "success", "message": "..."}
- Error: {"status": "error", "message": "..."}

## Error Codes
- 400: Bad request
- 401: Unauthorized
- 500: Internal server error

## Development Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run application: `python app.py`
3. Access API at: http://localhost:5000
