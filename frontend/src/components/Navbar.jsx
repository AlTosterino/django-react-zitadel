import { Link } from "react-router-dom";
import { useAuth } from "oidc-react";
export default function Navbar() {
  const { userData } = useAuth();
  const isLoggedIn = userData !== null;
  const { signIn, signOutRedirect } = useAuth();

  return (
    <div className="d-flex justify-content-between">
      <h1 className="">KeyCloak App</h1>
      <ul className="nav">
        <Link to="/" className="nav-link">
          Home
        </Link>
        <Link to="/login" className="nav-link" onClick={signIn}>
          Login
        </Link>
        <Link to="/logout" className="nav-link" onClick={signOutRedirect}>
          Logout
        </Link>
        {isLoggedIn && (
          <Link to="/resource" className="nav-link">
            Protected Resource
          </Link>
        )}
      </ul>
    </div>
  );
}
