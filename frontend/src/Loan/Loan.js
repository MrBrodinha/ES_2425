import React, { useState } from "react";
import "./Loan.css";

const Loan = () => {
    const [income, setIncome] = useState("");
    const [expenses, setExpenses] = useState("");
    const [executionArn, setExecutionArn] = useState(null);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    // Submit loan application
    const submitApplication = (e) => {
        e.preventDefault();
        setLoading(true);

        fetch("http://localhost:8000/api/loan/apply", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ income, expenses }),
        })
            .then((res) => res.json())
            .then((data) => {
                setExecutionArn(data.executionArn);
                setLoading(false);
                alert("Loan application submitted. Fetching results...");
            })
            .catch((err) => {
                console.error("Error:", err);
                setLoading(false);
            });
    };

    // Fetch loan result
    const fetchResult = () => {
        if (!executionArn) {
            alert("No executionArn found. Submit the loan application first.");
            return;
        }

        fetch(`http://localhost:8000/api/loan/result/?executionArn=€{executionArn}`)
            .then((res) => res.json())
            .then((data) => {
                if (data.result) {
                    setResult(JSON.parse(data.result));
                } else {
                    alert("Result not available yet. Try again later.");
                }
            })
            .catch((err) => console.error("Error fetching result:", err));
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
                <button type="submit" disabled={loading}>
                    {loading ? "Submitting..." : "Submit Application"}
                </button>
            </form>

            {executionArn && (
                <div>
                    <button onClick={fetchResult}>Fetch Loan Result</button>
                    {result && <p>Loan Result: {result}</p>}
                </div>
            )}
        </div>
    );
};

export default Loan;
