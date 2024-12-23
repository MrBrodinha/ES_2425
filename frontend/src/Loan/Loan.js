import React, { useState } from "react";
import "./Loan.css";

const Loan = () => {
    const [amount, setAmount] = useState(""); // Loan amount
    const [duration, setDuration] = useState(""); // Loan duration
    const [loading, setLoading] = useState(false);
    const [simulationResult, setSimulationResult] = useState(null);

    // Function to handle the loan simulation
    const handleSimulate = (e) => {
        e.preventDefault();
        setLoading(true);
        setSimulationResult(null); // Clear previous results

        // Make API request to the backend
        fetch("http://banco-env.eba-wexihakc.us-east-1.elasticbeanstalk.com/api/loan/simulate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                amount: parseFloat(amount),
                duration: parseInt(duration),
            }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.Result) {
                    setSimulationResult(JSON.parse(data.Result)); // Save the result
                } else {
                    alert("Simulation failed. Please try again.");
                }
                setLoading(false);
            })
            .catch((err) => {
                console.error("Error during simulation:", err);
                alert("An error occurred during the simulation.");
                setLoading(false);
            });
    };

    return (
        <div className="loan-page">
            <h1>Loan Simulation</h1>
            <form onSubmit={handleSimulate}>
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
                    {loading ? "Simulating..." : "Simulate"}
                </button>
            </form>

            {/* Display the simulation result */}
            {simulationResult && (
                <div className="simulation-result">
                    <h2>Simulation Result</h2>
                    <pre>{JSON.stringify(simulationResult, null, 2)}</pre>
                </div>
            )}
        </div>
    );
};

export default Loan;
