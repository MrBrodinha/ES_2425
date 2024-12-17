import React, { useEffect, useState } from "react";
import Navbar from "../Navbar/Navbar";
import { Link } from "react-router-dom";
import "./Home.css";

const Home = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Fetch data from if not error
        fetch("http://localhost:8000/api/home")
            .then((res) => res.json())
            .then((data) => {
                setData(data.message);
                setLoading(false);
            })
            .catch((error) => {
                console.error("Error:", error);
                setLoading(false);
            });
    }, []);

    return (
        <><Navbar />
        <div className="home-container">
            <div className="home-hero">
                <h1>Welcome to Aqua Bank</h1>
                <p>Your trusted partner for online loan applications.</p>
                <div className="home-buttons">
                    <Link to="/loan" className="btn btn-primary">
                        Start a Loan Simulation
                    </Link>
                    <br></br>
                    <Link to="/login" className="btn btn-secondary">
                        Login to Your Account
                    </Link>
                </div>
            </div>
            <div className="home-features">
                <h2>Why Choose Us?</h2>
                <div className="features-grid">
                    <div className="feature-item">
                        <h3>Fast Loan Approval</h3>
                        <p>Get quick responses with our streamlined loan process.</p>
                    </div>
                    <div className="feature-item">
                        <h3>Secure Authentication</h3>
                        <p>Your data is safe with our advanced security features.</p>
                    </div>
                    <div className="feature-item">
                        <h3>Simple Interface</h3>
                        <p>Our user-friendly interface makes loan applications easy.</p>
                    </div>
                </div>
            </div>
        </div></>
    );
}

export default Home;