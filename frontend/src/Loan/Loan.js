import React, { useState } from "react";
import "./Loan.css";

const Loan = () => {
    const [income, setIncome] = useState("");
    const [expenses, setExpenses] = useState("");
    const [amount, setAmount] = useState("");
    const [duration, setDuration] = useState(""); 
    const [executionArn, setExecutionArn] = useState(null);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const simulateLoan = (amount, duration) => {
        fetch("http://localhost:8000/api/loan/simulate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ amount, duration }),
        })
            .then((res) => res.json())
            .then((data) => {
                console.log("Simulation Result:", data);
            })
            .catch((err) => console.error("Error simulating loan:", err));
    };
    

    // Submit loan application
    const submitApplication = (e) => {
        e.preventDefault();
        setLoading(true);

        fetch("http://localhost:8000/api/loan/apply", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                income,
                expenses,
                amount,
                duration,
                user_id: "1", // Replace with the correct user ID
            }),
        })
            .then((res) => res.json())
            .then((data) => {
                setExecutionArn(data.executionArn);  // Store the execution ARN
                setLoading(false);
                alert("Loan application submitted. Fetching results...");
            })
            .catch((err) => {
                console.error("Error:", err);
                setLoading(false);
            });
    };

    // Fetch loan status
    const fetchLoanStatus = () => {
        if (!executionArn) {
            alert("No executionArn found. Submit the loan application first.");
            return;
        }

        // Call the 'api/loan/status' endpoint to check the status of the loan application using executionArn
        fetch(`http://localhost:8000/api/loan/status?loan_id=${executionArn}`)
            .then((res) => res.json())
            .then((data) => {
                if (data.Result) {
                    // If the result exists, display it
                    setResult(JSON.parse(data.Result));
                } else {
                    alert("Loan result not available yet. Please try again later.");
                }
            })
            .catch((err) => console.error("Error fetching loan status:", err));
    };

    

    return (
        <div className="loan-page">
            <h1>Loan Application</h1>

            <form onSubmit={submitApplication}>
                <label>Monthly Income (€):</label>
                <input
                    type="number"
                    value={income}
                    onChange={(e) => setIncome(e.target.value)}
                    required
                />
                <label>Monthly Expenses (€):</label>
                <input
                    type="number"
                    value={expenses}
                    onChange={(e) => setExpenses(e.target.value)}
                    required
                />
                <label>Loan Amount (€):</label>
                <input
                    type="number"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    required
                />
                <label>Loan Duration (Months):</label>
                <input
                    type="number"
                    value={duration}
                    onChange={(e) => setDuration(e.target.value)}
                    required
                />
                <button type="submit" disabled={loading}>
                    {loading ? "Submitting..." : "Submit Application"}
                </button>
            </form>

            {executionArn && (
                <div>
                    <button onClick={fetchLoanStatus}>Fetch Loan Status</button>
                    {result && <p>Loan Result: {JSON.stringify(result)}</p>}
                </div>
            )}
        </div>
    );
};

export default Loan;
