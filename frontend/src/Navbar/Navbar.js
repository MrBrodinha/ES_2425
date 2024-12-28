import React from "react";
import { Link } from "react-router-dom";
import "./Navbar.css"; // Import CSS for styling

const Navbar = () =>
{
    const token = localStorage.getItem("token");

    var isLoggedIn = false;

    if (token)
    {
        isLoggedIn = true;
    }

    const logout = () =>
    {
        localStorage.removeItem("token");
        localStorage.removeItem("hasPermissions");
        window.location.href = "/";
    }

    return (
        <nav className="navbar">
            <div className="logo">
                <Link to="/">Aqua Bank</Link>
            </div>
            <ul className="nav-links">
                <li>
                    <Link to="/">Home</Link>
                </li>
                { !isLoggedIn && (
                    <li>
                        <Link to="/login">Login</Link>
                    </li>
                ) }
                { isLoggedIn && (
                    <li>
                        <Link to="/" onClick={ logout }>Logout</Link>
                    </li>
                ) }
            </ul>
        </nav>
    );
};

export default Navbar;
