import React, { useCallback, useRef, useState, useEffect } from "react";
import Navbar from "../Navbar/Navbar";
import "./Loan.css";
import Webcam from 'react-webcam';


const Loan = () =>
{
    const token = localStorage.getItem("token");

    const [amount, setAmount] = useState(""); // Loan amount
    const [ duration, setDuration ] = useState(""); // Loan duration
    const [ yearly_income, setYearlyIncome ] = useState(""); // Yearly income
    const [loading, setLoading] = useState(false);
    const [ simulationResult, setSimulationResult ] = useState(null);
    const [ pic, setPic ] = useState(false);
    const [ isLoggedIn, setIsLoggedIn ] = useState(false);
    const [ nextDocument, setnextDocument ] = useState(false);
    const [ sendLoan, setSendLoan ] = useState(false);

    useEffect(() =>
    {
        if (token)
        {
            setIsLoggedIn(true);
        }
    }, [ token ]);
    
    // webcam
    const webcamRef = useRef(null);
    const [ imgSrc, setImgSrc ] = useState(null);

    // create a capture function
    const capture = useCallback(() =>
    {
        const imageSrc = webcamRef.current.getScreenshot();
        setImgSrc(imageSrc);
    }, [ webcamRef ]);

    const retake = () =>
    {
        setImgSrc(null);
    };

    // Function to handle the loan simulation
    const handleSimulate = (e) => {
        e.preventDefault();
        setLoading(true);
        setSimulationResult(null); // Clear previous results

        // Make API request to the backend
        fetch(process.env.REACT_APP_API_URL + "/api/loan/simulate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                amount: parseFloat(amount),
                duration: parseInt(duration),
                yearly_income: parseFloat(yearly_income)
            }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.Result)
                {
                    setSimulationResult(data.Result); // Save the result
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

    const handleConfirmPic = (e) => {
        e.preventDefault();
        setLoading(true);

        // Make API request to the backend
        fetch(process.env.REACT_APP_API_URL + "/api/loan/verify_face", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                photo: imgSrc,
                token: token
            }),
        })
            .then((response) => response.json())
            .then((data) =>
            {
                if (data.confirmation)
                {
                    setnextDocument(true);
                } else
                {
                    alert(data.message || "An error occurred");
                }
                setLoading(false);
            })
            .catch((err) =>
            {
                alert("An error occurred during the face detection.");
                setLoading(false);
            });
    };
        
    const handleProceed = () =>
    {
        // go to home
        if (!isLoggedIn)
            window.location.href = "/login";

        else
            setPic(true);
    };

    const submitLoan = (e) =>
    {
        e.preventDefault();
        setLoading(true);

        // Make API request to the backend
        fetch(process.env.REACT_APP_API_URL + "/api/loan/apply", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                token: token,
                yearly_income: parseFloat(yearly_income),
                amount: parseFloat(amount),
                duration: parseInt(duration),
                monthly_payment: parseFloat(simulationResult.monthly_payment),
                answer: simulationResult.answer
            }),
        })
            .then((response) => response.json())
            .then((data) =>
            {
                if (data.confirmation)
                {
                    setTimeout(() => { window.close(); }, 5000);
                } else
                {
                    console.log(data);
                }
                setLoading(false);
            })
            .catch((err) =>
            {
                alert("An error occurred during the loan submission.");
                setLoading(false);
            });
    };

    const submitDocuments = (e) =>
    {
        e.preventDefault();
        setLoading(true);

        const formData = new FormData();
        formData.append("annual_income", e.target[ 0 ].files[ 0 ]); // First file input
        formData.append("self_declaration", e.target[ 1 ].files[ 0 ]); // Second file input
        formData.append("token", token); // Add token to form data

        // Make API request to the backend
        fetch(process.env.REACT_APP_API_URL + "/api/loan/submit_documents", {
            method: "POST",
            body: formData, // FormData object
        })
            .then((response) => response.json())
            .then((data) =>
            {
                if (data.confirmation)
                {
                    setSendLoan(true);
                    alert("Your Loan Request has been submitted, a loan officer will look into it");
                    submitLoan(e);
                    window.open("/", "_blank");

                } else
                {
                    alert(data.message || "An error occurred");
                }
                setLoading(false);
            })
            .catch((err) =>
            {
                alert("An error occurred during the document submission.");
                setLoading(false);
            });
    };


    return (
        <><Navbar />
            <div className="loan-page">
                {/* Display the loan simulation form */ }
                { !simulationResult && (
                    <div className="loan-simulation">
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

                    <label>Yearly Income (€):</label>
                    <input
                        type="number"
                        value={yearly_income}
                        onChange={(e) => setYearlyIncome(e.target.value)}
                        required
                    />

                    <button type="submit" disabled={loading}>
                        {loading ? "Simulating..." : "Simulate"}
                    </button>
                        </form>
                    </div>
            )}
            {/* Display the simulation result */ }
            { simulationResult && !pic && !nextDocument && (
                <div className="simulation-result">
                    <h2>Simulation Result</h2>
                        <p><strong>Simulation Result:</strong> { simulationResult.answer }</p>
                        <p><strong>Estimated Monthly Payment:</strong> { simulationResult.monthly_payment }€</p>

                    {/* Show the "Proceed" button only if the answer is "accept" */ }
                    { simulationResult.answer === "ACCEPTED" && isLoggedIn && !nextDocument && (
                        <button onClick={ handleProceed }>Proceed with loan request</button>
                        ) }
                    { simulationResult.answer === "ACCEPTED" && !isLoggedIn &&(
                        <button onClick={ handleProceed }>You need to Log in!</button>
                    ) }
                </div>
                ) }
                
                {/* webcam */ }
                { pic && !nextDocument && (
                <div className="confirm-identify">
                    <h2>Confirm your identity</h2>        
                    <div className="container" style={ { width: '100%', height: '100%' } }>
                        { imgSrc ? (
                            <img src={ imgSrc } alt="webcam" />
                        ) : (
                                <Webcam screenshotFormat="image/jpeg" height="100%" width="100%" ref={ webcamRef } />
                        ) }
                        <div className="btn-container">
                            { imgSrc ? (
                            <div>
                                <button type="button" onClick={ retake }>Retake photo</button>
                                <br />
                                        <button type="button" onClick={ handleConfirmPic } disabled={ loading }>
                                            { loading ? "Confirming..." : "Confirm" }
                                        </button>
                            </div>
                            ) : (
                                <button type="button" onClick={ capture }>Capture photo</button>
                            ) }
                        </div>
                    </div>
                </div>
                ) }
                { !sendLoan && nextDocument && (
                    // upload two files, anual income comprovative and self declaration, limit size to 1mb per document
                    <div className="upload-documents">
                        <h2>Upload Documents</h2>
                        <form onSubmit={ submitDocuments }>
                            <label>Annual Income Comprovative</label>
                            <input type="file" accept=".pdf" required />
                            <label>Self Declaration</label>
                            <input type="file" accept=".pdf" required />
                            <button type="submit" disable={ loading }>
                                { loading ? "Uploading..." : "Upload" }
                            </button>
                        </form>
                    </div>
                ) }
                { sendLoan && (
                    //create empty page saying "DO NOT CLOSE THIS PAGE, IT WILL CLOSE ON ITS OWN"
                    <div className="send-loan">
                        <h2>Loan Request Sent</h2>
                        <p>Do not close this page, it will close on its own</p>
                    </div>) }
            </div>
        </>
    );
};

export default Loan;
