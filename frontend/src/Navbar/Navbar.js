import React from "react";
import { Link } from "react-router-dom";
import "./Navbar.css"; // Import CSS for styling

const Navbar = () => {
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
                    <Link to="/login">Login</Link>
                </li>
                <li>
                    <Link to="/loan">Loans</Link>
                </li>
            </ul>
        </nav>
    );
};

export default Navbar;
