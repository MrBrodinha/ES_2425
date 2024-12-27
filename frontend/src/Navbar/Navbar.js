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
        window.location.href = "/";
    }

    if (!isLoggedIn) {
        return (
            <nav className="navbar">
                <div className="logo">
                    <Link to="/">Aqua Bank</Link>
                </div>
                <ul className="nav-links">
                    <li>
                        <Link to="/">Home</Link>
                    </li>
                    <li>
                        <Link to="/loan">Simulate Loans</Link>
                    </li>
                    <li>
                        <Link to="/login">Login</Link>
                    </li>

                </ul>
            </nav>
        );
    } else {
        return (
            <nav className="navbar">
                <div className="logo">
                    <Link to="/">Aqua Bank</Link>
                </div>
                <ul className="nav-links">
                    <li>
                        <Link to="/">Home</Link>
                    </li>
                    <li>
                        <Link to="/loan">Simulate Loans</Link>
                    </li>
                    <li>
                        <Link to="/" onClick={logout}>Logout</Link>
                    </li>
                </ul>
            </nav>
        );
    }
};

export default Navbar;
