import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import Navbar from "../Navbar/Navbar";

const LoanDetails = () =>
{
    const location = useLocation();

    const token = localStorage.getItem("token");
    const [ isLoggedIn, setIsLoggedIn ] = useState(false);
    

    //GET loan_id
    const urlParams = new URLSearchParams(location.search);
    const loan_id = urlParams.get('loan_id');

    const [ loan, setLoan ] = useState(null); // Change loan state to object

    

    // UseEffect to fetch loan data once when the component is mounted or loan_id changes
    useEffect(() =>
    {
        const fetchLoanData = async () =>
        {
            if (loan_id && token)
            {
                try
                {
                    const response = await fetch(`${ process.env.REACT_APP_API_URL }/api/loans?token=${ token }&loan_id=${ loan_id }`);
                    const data = await response.json();

                    console.log("Fetched loan:", data);

                    if (data.loans_status)
                    {
                        console.log("Setting loan data:", data.loans_status);
                        setLoan(data.loans_status);
                    } else
                    {
                        console.error("Error fetching loan data:", data.message);
                    }
                } catch (error)
                {
                    console.error("Error fetching loan data:", error);
                }
            }
        };

        // Fetch only when loan_id and token are valid and loan is not already set
        if (!loan)
        {
            fetchLoanData();
        }
    }, [ loan_id, token, loan ]);// Run this effect only when loan_id or token changes

    // Handle interview slot selection
    

    useEffect(() =>
    {
        if (token)
        {
            setIsLoggedIn(true);
        }
    }, [ token ]); // Access the loan data from state

    

    console.log(loan)
    if (!loan) return <div>Loading...</div>; // Show loading while fetching loan data
 
    return (
        <>
            <Navbar />
            <div className="feature-item">
                <h3>Loan ID: { loan.id }</h3>
                <p><strong>Status:</strong> { loan.status }</p>
                <p>------</p>
                <p><strong>Amount:</strong> ${ loan.amount }</p>
                <p><strong>Duration:</strong> { loan.duration } months</p>
                <p>------</p>
                <p><strong>Monthly Payment:</strong> ${ loan.monthly_payment }</p>
                <p><strong>Total Paid:</strong> ${ loan.total_paid }</p>
                <p><strong>Total Payment:</strong> ${ loan.monthly_payment * loan.duration }</p>
            </div>

            { loan.status === "ACCEPTED" && loan.total_paid < (loan.monthly_payment * loan.duration) && (
                <button className="btn btn-primary" onClick={ handlePay }>Pay</button>
            ) }

            { loan.status === "CHOOSE INTERVIEW" && (
                <button className="btn btn-primary" onClick={ handleGrabInterviews }>Grab Interviews</button>
            ) }

            { interviews.length > 0 && loan.status === "CHOOSE INTERVIEW" && (
                <div>
                    <h3>Interviews</h3>
                    <div>
                        { interviews.map((interview) => (
                            <div key={ interview.id }>
                                <p><strong>Day:</strong> { interview.day }</p>
                                <p><strong>Time:</strong> { new Date(interview.time * 1000).toISOString().slice(11, 16) }</p>
                                <button
                                    onClick={ () => handleSlotSelect(interview.id) }
                                    style={ {
                                        backgroundColor: selectedSlot === interview.id ? 'green' : 'lightgrey',
                                        color: 'white'
                                    } }
                                >
                                    { selectedSlot === interview.id ? 'Selected' : 'Select' }
                                </button>
                                <p>------</p>
                            </div>
                        )) }
                        <button onClick={ handleButtonClick }>Confirm Selection</button>
                    </div>
                </div>
            ) }

            { loan.status === "INTERVIEW PENDING" && (
                <div>
                    <h3>Interview</h3>
                    { interviews.map((interview) => (
                        <div key={ interview.id }>
                            <p><strong>Day:</strong> { interview.day }</p>
                            <p><strong>Time:</strong> { new Date(interview.time * 1000).toISOString().slice(11, 16) }</p>
                        </div>
                    )) }
                </div>
            ) }
        </>
    );
};

export default LoanDetails;
