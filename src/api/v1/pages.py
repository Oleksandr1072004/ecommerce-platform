from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from src.core.security import get_current_user, get_current_user_cookie
from src.models.user import User

router = APIRouter(tags=["pages"])


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(current_user: User = Depends(get_current_user_cookie)) -> str:
    logout_form = """
        <form method="post" action="/api/v1/auth/logout" style="margin-top:20px">
            <button type="submit">Logout</button>
        </form>
    """

    if current_user.role.value == "admin":
        return f"""
        <html><body style="font-family:sans-serif;max-width:600px;margin:50px auto">
          <h1>Admin Dashboard</h1>
          <p>Welcome, {current_user.email}</p>
          <ul>
            <li><a href="/docs">API docs</a></li>
            <li><a href="/api/v1/admin/users">Manage users</a></li>
          </ul>
          {logout_form}
        </body></html>
        """

    return f"""
    <html><body style="font-family:sans-serif;max-width:600px;margin:50px auto">
      <h1>Customer Dashboard</h1>
      <p>Welcome, {current_user.email}</p>
      <ul>
        <li><a href="/api/v1/products">Browse products</a></li>
        <li><a href="/api/v1/auth/me">My profile</a></li>
      </ul>
      {logout_form}
    </body></html>
    """