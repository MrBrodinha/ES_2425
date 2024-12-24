import React, { useState } from "react";
import "./Login.css"; // Import the CSS file for styling
import Navbar from "../Navbar/Navbar";

const Login = () => {
    const [ email, setEmail ] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleLogin = (e) =>
    {
        e.preventDefault();
        setLoading(true);
        setError(null);

        // Simulate login API request
        fetch("http://localhost:8000/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
        })
            .then((response) =>
            {
                console.log("Response status:", response.status); // Log response status
                if (!response.ok)
                {
                    throw new Error("Invalid credentials");
                }
                return response.json();
            })
            .then((data) =>
            {
                console.log("Response data:", data); // Log the received data
                if (data.username)
                {
                    alert(`Welcome, ${ data.username }!`);
                    setLoading(false);
                } else
                {
                    setError(data.message || "An error occurred");
                    setLoading(false);
                }
            })
            .catch((error) =>
            {
                console.error("Error:", error); // Log error
                setError(error.message);
                setLoading(false);
            });
    };


    return (
        <><Navbar />
        <div className="login-container">
            <div className="login-card">
                <h2>Login</h2>
                <form onSubmit={handleLogin}>
                    <div className="form-group">
                        <label htmlFor="email">E-mail</label>
                        <input
                            type="text"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required />
                    </div>
                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required />
                    </div>
                    {error && <p className="error-message">{error}</p>}
                    <button type="submit" className="login-button" disabled={loading}>
                        {loading ? "Logging in..." : "Login"}
                    </button>
                    <div className="register-link">
                        Don't have an account? <a href="/register">Register</a>
                    </div>
                </form>
            </div>
        </div></>
    );
};

export default Login;
