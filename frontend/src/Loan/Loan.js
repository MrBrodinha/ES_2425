import React, { useState } from "react";
import "./Loan.css";
import Navbar from "../Navbar/Navbar";

const Loan = () => {
    // State variables
    const [loanAmount, setLoanAmount] = useState("");
    const [loanDuration, setLoanDuration] = useState("");
    const [monthlyPayment, setMonthlyPayment] = useState(null);
    const [isLoggedIn, setIsLoggedIn] = useState(false); // Placeholder for login
    const [income, setIncome] = useState("");
    const [expenses, setExpenses] = useState("");
    const [result, setResult] = useState(null);

    // Simulate loan calculation
    const handleSimulateLoan = () => {
        if (loanAmount && loanDuration) {
            const payment = (loanAmount * 1.05) / loanDuration; // Simple calculation
            setMonthlyPayment(payment.toFixed(2));
        } else {
            alert("Please enter valid loan amount and duration.");
        }
    };

    // Placeholder for login
    const handleLogin = () => {
        alert("Placeholder: Facial recognition not implemented yet.");
        setIsLoggedIn(true);
    };

    // Handle loan application submission
    const handleSubmitApplication = (e) => {
        e.preventDefault();
        if (income && expenses) {
            // Placeholder: Logic for determining "accept", "interview", or "reject"
            const randomOutcome = ["Accept", "Interview", "Reject"];
            const randomIndex = Math.floor(Math.random() * 3);
            setResult(randomOutcome[randomIndex]);
        } else {
            alert("Please fill in all required fields.");
        }
    };

    return (
        <><Navbar />
        <div className="loan-page">
            <h1>Loan Page</h1>

            {/* Loan Simulator */}
            <section className="loan-section">
                <h2>Loan Simulator</h2>
                <label>Loan Amount (€):</label>
                <input
                    type="number"
                    value={loanAmount}
                    onChange={(e) => setLoanAmount(e.target.value)}
                    placeholder="Enter loan amount"
                />
                <label>Loan Duration (months):</label>
                <input
                    type="number"
                    value={loanDuration}
                    onChange={(e) => setLoanDuration(e.target.value)}
                    placeholder="Enter duration in months"
                />
                <button onClick={handleSimulateLoan}>Simulate</button>
                {monthlyPayment && (
                    <p>Estimated Monthly Payment: €{monthlyPayment}</p>
                )}
            </section>

            {/* Login Placeholder */}
            {!isLoggedIn && (
                <section className="loan-section">
                    <h2>Login to Continue</h2>
                    <button onClick={handleLogin}>Log in with Facial Recognition</button>
                </section>
            )}

            {/* Loan Application Form */}
            {isLoggedIn && (
                <section className="loan-section">
                    <h2>Loan Application</h2>
                    <form onSubmit={handleSubmitApplication}>
                        <label>Monthly Income (€):</label>
                        <input
                            type="number"
                            value={income}
                            onChange={(e) => setIncome(e.target.value)}
                            placeholder="Enter your monthly income"
                            required
                        />
                        <label>Monthly Expenses (€):</label>
                        <input
                            type="number"
                            value={expenses}
                            onChange={(e) => setExpenses(e.target.value)}
                            placeholder="Enter your monthly expenses"
                            required
                        />
                        <button type="submit">Submit Application</button>
                    </form>
                    {result && <p>Application Result: {result}</p>}
                </section>
            )}
        </div></>
    );
};

export default Loan;
