from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["pages"])


LOGIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login — Ecommerce Platform</title>
    <style>
        body { font-family: system-ui, sans-serif; max-width: 400px; margin: 80px auto; padding: 20px; }
        input { width: 100%; padding: 8px; margin: 4px 0 12px; box-sizing: border-box; }
        button { padding: 10px 16px; cursor: pointer; }
        .error { color: crimson; margin-top: 12px; }
        a { display: inline-block; margin-top: 16px; }
    </style>
</head>
<body>
    <h1>Sign in</h1>
    <form id="loginForm">
        <label>Email
            <input type="email" name="email" required autofocus>
        </label>
        <label>Password
            <input type="password" name="password" required>
        </label>
        <button type="submit">Sign in</button>
    </form>
    <div class="error" id="msg"></div>
    <a href="/register">Don't have an account? Register</a>

    <script>
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = Object.fromEntries(new FormData(e.target));

        const res = await fetch('/api/v1/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
            credentials: 'same-origin',
        });

        if (res.ok) {
            window.location.href = '/dashboard';
        } else {
            let detail = 'Login failed';
            try { detail = (await res.json()).detail || detail; } catch {}
            document.getElementById('msg').textContent = detail;
        }
    });
    </script>
</body>
</html>
"""


REGISTER_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Register — Ecommerce Platform</title>
    <style>
        body { font-family: system-ui, sans-serif; max-width: 400px; margin: 80px auto; padding: 20px; }
        input { width: 100%; padding: 8px; margin: 4px 0 12px; box-sizing: border-box; }
        button { padding: 10px 16px; cursor: pointer; }
        .error { color: crimson; margin-top: 12px; }
        a { display: inline-block; margin-top: 16px; }
    </style>
</head>
<body>
    <h1>Create account</h1>
    <form id="registerForm">
        <label>Email
            <input type="email" name="email" required autofocus>
        </label>
        <label>Full name
            <input type="text" name="full_name">
        </label>
        <label>Password (min 8 chars)
            <input type="password" name="password" minlength="8" required>
        </label>
        <button type="submit">Register</button>
    </form>
    <div class="error" id="msg"></div>
    <a href="/login">Already have an account? Sign in</a>

    <script>
    document.getElementById('registerForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = Object.fromEntries(new FormData(e.target));
        if (!data.full_name) delete data.full_name;

        const res = await fetch('/api/v1/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        if (res.ok) {
            window.location.href = '/login';
        } else {
            let detail = 'Registration failed';
            try { detail = (await res.json()).detail || detail; } catch {}
            document.getElementById('msg').textContent = JSON.stringify(detail);
        }
    });
    </script>
</body>
</html>
"""


@router.get("/login", response_class=HTMLResponse)
def login_page() -> str:
    return LOGIN_HTML


@router.get("/register", response_class=HTMLResponse)
def register_page() -> str:
    return REGISTER_HTML