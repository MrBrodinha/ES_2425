import React, { useState, useEffect } from "react";
import Navbar from "../Navbar/Navbar";
import { Link } from "react-router-dom";
import "./Home.css";

const Home = () =>
{
    const token = localStorage.getItem("token");

    const [ isLoggedIn, setIsLoggedIn ] = useState(false);
    const [ hasLoans, setHasLoans ] = useState(false);
    const [ loans , setLoans ] = useState([]);
    
    useEffect(() =>
    {
        if (token)
        {
            setIsLoggedIn(true);
        }
    }, [ token ]);

    useEffect(() =>
    {
        const handleLoanCheck = async () =>
        {
            try
            {
                const response = await fetch(
                    process.env.REACT_APP_API_URL + '/api/loans?token=' + token);
                const data = await response.json();
                console.log('Fetched loans:', data);  // Log the fetched data
                if (data.loans_status)
                {
                    setHasLoans(true);
                    setLoans(data.loans_status);
                }
            } catch (error)
            {
                console.error("Error fetching loans:", error);
            }
        };

        if (isLoggedIn)
        {
            handleLoanCheck();
        }
    }, [ isLoggedIn, token ]);

    const handleLoanClick = (loan) =>
    {
        window.location.href = "/LoanDetails?loan_id=" + loan;
    };


    return (
        <>
            <Navbar />
            { !hasLoans && (
                <div className="home-container">
                    <div className="home-hero">
                        <h1>Welcome to Aqua Bank</h1>
                        <p>Your trusted partner for online loan applications.</p>
                        <div className="home-buttons">
                            <Link to="/loan" className="btn btn-primary">
                                Start a Loan Simulation
                            </Link>
                            <br></br>
                            { !isLoggedIn && (
                                <Link to="/login" className="btn btn-secondary">
                                    Login to Your Account
                                </Link>
                            )}
                                
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
                </div>
            ) }
            { hasLoans && (
                <div className="home-container">
                    <div className="home-hero">
                        <div className="home-buttons">
                            <Link to="/loan" className="btn btn-primary">
                                Start a Loan Simulation
                            </Link>
                        </div>
                    </div>
                    <div className="home-features">
                        <h2>Your Loan Applications</h2>
                        <div className="features-grid">
                            { loans.map((loan, index) => (
                                <div className="feature-item"
                                    key={ index }
                                    onClick={ () => handleLoanClick(loan[ 0 ]) }
                                    style={ { cursor: "pointer", border: "1px solid #ccc", padding: "10px", margin: "10px" } } >
                                        <h3>Loan ID: { loan[ 0 ] }</h3>
                                        <p><strong>Status:</strong> { loan[ 6 ] }</p>
                                        <p>------</p>
                                        <p><strong>Amount:</strong> ${ loan[ 3 ] }</p>
                                        <p><strong>Duration:</strong> { loan[ 4 ] } months</p>
                                        <p>------</p>
                                        <p><strong>Monthly Payment:</strong> ${ loan[ 5 ] }</p>
                                        <p><strong>Total Paid:</strong> ${ loan[ 8 ] }</p>
                                        <p><strong>Total Payment:</strong> ${ loan[ 5 ] * loan[ 4 ] }</p>
                                </div>
                            )) }
                        </div>
                    </div>
                </div>
            )}
        </>
    );
};

export default Home;