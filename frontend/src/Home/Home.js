import React, { useState, useEffect } from "react";
import Navbar from "../Navbar/Navbar";
import { Link } from "react-router-dom";
import "./Home.css";

const Home = () =>
{
    const token = localStorage.getItem("token");
    const hasPermissions = localStorage.getItem("hasPermissions");
    const [ isLoggedIn, setIsLoggedIn ] = useState(false);

    useEffect(() =>
    {
        if (token)
        {
            setIsLoggedIn(true);
        }
    }, [ token ]);

    const [ hasLoans, setHasLoans ] = useState(false);
    const [ loans, setLoans ] = useState([]);

    const [ isSingleLoan, setIsSingleLoan ] = useState(false);
    const [ singleLoan, setSingleLoan ] = useState([]);

    const [ client, setClient ] = useState([]);

    const [ hasEmptyLoans, setHasEmptyLoans ] = useState(false);
    const [ emptyLoans, setEmptyLoans ] = useState([]);

    // For interview
    const [ selectedSlot, setSelectedSlot ] = useState(null);
    const [ interviews, setInterviews ] = useState([]);

    const [ chooseInterviews, setChooseInterviews ] = useState(false);

    // LOAN OFFICER --------------------------------------
    const handleNewLoanCheck = async (loan_officer_id) =>
    {
        try
        {
            const response = await fetch(
                process.env.REACT_APP_API_URL + '/api/loan_officer/loans?token=' + token + '&loan_officer_id=' + loan_officer_id);
            const data = await response.json();
            console.log('Fetched loans:', data);  // Log the fetched data
            if (data.loans)
            {
                // eslint-disable-next-line
                if (data.loans.length != 0)
                    if (loan_officer_id === 0)
                    {
                        setHasEmptyLoans(true);
                        setEmptyLoans(data.loans);
                    } else
                    {
                        setHasLoans(true);
                        setLoans(data.loans);
                    }
                else
                {
                    alert("No Loans!")
                }
            }
        } catch (error)
        {
            console.error("Error fetching loans:", error);
        }
    }

    const handleLoanClick = async (loan) =>
    {
        try
        {
            const response = await fetch(process.env.REACT_APP_API_URL + "/api/loans?token=" + token + "&loan_id=" + loan);
            const data = await response.json();

            console.log("Fetched loan:", data);

            if (data.loan_status)
            {
                setSingleLoan(data.loan_status);
                setIsSingleLoan(true);
            } else
            {
                console.error("Error fetching loan data:", data.message);
            }
        } catch (error)
        {
            console.error("Error fetching loan data:", error);
        }
    };

    const handleLoanAction = async (loan, answer) =>
    {
        try
        {
            if (answer === "ACCEPTED" || answer === "REJECTED")
                alert("Updating loan status, could take a while...");
            const response = await fetch(
                process.env.REACT_APP_API_URL + "/api/loan/assign",
                {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ token: token, loan_id: loan, answer: answer }), // Assuming loan is an object with `id`
                }
            );
            const data = await response.json();
            if (data.confirm)
            {
                if (answer === "ACCEPTED" || answer === "REJECTED")
                    alert("Loan status updated successfully! Could take a while to reflect.");
            } else
            {
                alert("Error updating loan status. Please try again later.");
            }
        }
        catch (error)
        {
            console.error("Error updating loan status:", error);
        }

        if (answer === "ACCEPTED" || answer === "REJECTED")
        {
            try
            {
                const response = await fetch(
                    process.env.REACT_APP_API_URL + "/api/loan/interviews/remove",
                    {
                        method: "DELETE",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({ token: token, loan_id: loan }), // Assuming loan is an object with `id`
                    }
                );
                const data = await response.json();
                if (data.confirmation)
                {
                    window.location.reload();
                } else
                {
                    alert("Error removing interview. Please try again later.");
                }
            }
            catch (error)
            {
                console.error("Error removing interview:", error);
            }
        }
    };

    const handleClientInformation = async (client_id, loan_id) =>
    {
        try
        {
            const response = await fetch(
                process.env.REACT_APP_API_URL + '/api/user/info?token=' + token + '&user_id=' + client_id + "&loan_id=" + loan_id);
            const data = await response.json();
            console.log('Fetched client:', data);  // Log the fetched data
            if (data)
            {
                setClient(data);
            }
        }
        catch (error)
        {
            console.error("Error fetching client:", error);
        }

        handleLoanClick(loan_id);
    };

    const handleGrabInterviews = async () =>
    {
        try
        {
            const response = await fetch(
                process.env.REACT_APP_API_URL + "/api/loan/interviews?token=" + token + "&loan_id=" + singleLoan[ 0 ]
            );
            const data = await response.json();
            console.log("Fetched interviews:", data);
            if (data.interviews)
            {
                setInterviews(data.interviews);

                // eslint-disable-next-line
                if (data.interviews.length == 0)
                    alert("No interviews available for this loan yet.");
            }
        } catch (error)
        {
            console.error("Error grabbing interviews:", error);
        }
    };

    const handleAddInterview = async (loan_id, interview_day, interview_time) =>
    {
        try
        {
            const response = await fetch(
                process.env.REACT_APP_API_URL + "/api/loan/interview/add",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ token: token, loan_id: loan_id, interview_day: interview_day, interview_time: interview_time }), // Assuming loan is an object with `id`
                }
            );
            const data = await response.json();
            if (data.confirmation)
            {
                handleGrabInterviews();
                alert("Interview added successfully! Could take a while to reflect.");
            } else
            {
                alert("Error adding interview. Please try again later.");
            }
        }
        catch (error)
        {
            console.error("Error adding interview:", error);
        }
    }

    const handleDeleteInterview = async (interview_id) =>
    {
        try
        {
            const response = await fetch(
                process.env.REACT_APP_API_URL + "/api/loan/interview/remove",
                {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ token: token, slot_id: interview_id }), // Assuming loan is an object with `id`
                }
            );
            const data = await response.json();
            if (data.confirmation)
            {
                handleGrabInterviews();
                alert("Interview removed successfully! Could take a while to reflect.");
            } else
            {
                alert("Error removing interview. Please try again later.");
            }
        }
        catch (error)
        {
            console.error("Error removing interview:", error);
        }
    }

    if (hasPermissions === "1")
    {
        return (
            <>
                <Navbar />
                <div className="home-container">
                    <div className="home-hero">
                        <h1>Welcome Loan Officer</h1>
                        <p>Navigating Lending Success with Aqua Bank!</p>
                        <div className="home-buttons">
                            { !hasEmptyLoans && !hasLoans && (
                                <button onClick={ () => handleNewLoanCheck(0) }>Show New Loan Applications</button>
                            ) }
                            { hasEmptyLoans && !isSingleLoan && (
                                <button onClick={ () =>
                                {
                                    setHasEmptyLoans(false);
                                    setEmptyLoans([]);
                                } }>Hide New Loan Applications</button>
                            ) }
                            <br></br>
                            { !hasLoans && !hasEmptyLoans && (
                                <button onClick={ () => handleNewLoanCheck(1) }>Show Associated Loan Applications</button>
                            ) }
                            { hasLoans && !isSingleLoan && (
                                <button onClick={ () =>
                                {
                                    setHasLoans(false);
                                    setLoans([]);
                                }
                                }>Hide Associated Loan Applications</button>
                            ) }
                            { isSingleLoan && (
                                <button onClick={ () =>
                                {
                                    setIsSingleLoan(false);
                                    setSingleLoan([]);
                                    setClient([]);
                                    setInterviews([]);
                                    setChooseInterviews(false);
                                }
                                }>Hide Loan Details</button>
                            ) }
                        </div>
                    </div>
                    { hasLoans && !isSingleLoan && (
                        <div className="home-features">
                            <h2>Your Associated Loan Applications</h2>
                            <div className="features-grid">
                                { loans.map((loan, index) => (
                                    <div className="feature-item"
                                        key={ index }
                                        onClick={ () =>
                                        {
                                            handleClientInformation(loan[ 1 ], loan[ 0 ]);
                                        } }
                                        style={ { cursor: "pointer", border: "1px solid #ccc", padding: "10px", margin: "10px" } } >
                                        <h3>Loan ID: { loan[ 0 ] }</h3>
                                        <p><strong>Client ID:</strong> { loan[ 1 ] }</p>
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
                    ) }
                    { hasEmptyLoans && !isSingleLoan && (
                        <div className="home-features">
                            <h2>New Loan Applications</h2>
                            <div className="features-grid">
                                { emptyLoans.map((emptyLoans, index) => (
                                    <div className="feature-item"
                                        key={ index }
                                        onClick={ () =>
                                        {
                                            handleClientInformation(emptyLoans[ 1 ], emptyLoans[ 0 ]);
                                        } }
                                        style={ { cursor: "pointer", border: "1px solid #ccc", padding: "10px", margin: "10px" } } >
                                        <h3>Loan ID: { emptyLoans[ 0 ] }</h3>
                                        <p><strong>Client ID:</strong> { emptyLoans[ 1 ] }</p>
                                        <p><strong>Status:</strong> { emptyLoans[ 6 ] }</p>
                                        <p>------</p>
                                        <p><strong>Amount:</strong> ${ emptyLoans[ 3 ] }</p>
                                        <p><strong>Duration:</strong> { emptyLoans[ 4 ] } months</p>
                                        <p>------</p>
                                        <p><strong>Monthly Payment:</strong> ${ emptyLoans[ 5 ] }</p>
                                        <p><strong>Total Paid:</strong> ${ emptyLoans[ 8 ] }</p>
                                        <p><strong>Total Payment:</strong> ${ emptyLoans[ 5 ] * emptyLoans[ 4 ] }</p>
                                    </div>
                                )) }
                            </div>
                        </div>
                    ) }
                    { isSingleLoan && (
                        <div className="home-features">
                            <h2>Loan ID: { singleLoan[ 0 ] }</h2>
                            <div className="features-grid">
                                <div className="feature-item">
                                    <p><strong>Status:</strong> { singleLoan[ 6 ] }</p>
                                    <p>------</p>
                                    <p><strong>Amount:</strong> ${ singleLoan[ 3 ] }</p>
                                    <p><strong>Duration:</strong> { singleLoan[ 4 ] } months</p>
                                    <p>------</p>
                                    <p><strong>Monthly Payment:</strong> ${ singleLoan[ 5 ] }</p>
                                    <p><strong>Total Paid:</strong> ${ singleLoan[ 8 ] }</p>
                                    <p><strong>Total Payment:</strong> ${ singleLoan[ 5 ] * singleLoan[ 4 ] }</p>
                                </div>
                                <div className="feature-item">
                                    <p><strong>Client ID:</strong> { client.user.id }</p>
                                    <p><strong>Client Username:</strong> { client.user.username }</p>
                                    <p><strong>Client Email:</strong> { client.user.email }</p>
                                    <p><strong>Client Credit Score:</strong> { client.user.credit_score }</p>
                                    <p><a href={ client.anual_income_url }>Annual Income</a></p>
                                    <p><a href={ client.self_declaration_url }>Self Declaration</a></p>
                                </div>
                            </div>
                        </div>
                    ) }
                    { isSingleLoan && singleLoan[ 6 ] !== "PAID" && singleLoan[ 6 ] !== "ACCEPTED" && singleLoan[ 6 ] !== "REJECTED" && (
                        <div>
                            <button onClick={ () => handleLoanAction(singleLoan[ 0 ], "ACCEPTED") }>ACCEPT</button>
                            <button onClick={ () => handleLoanAction(singleLoan[ 0 ], "REJECTED") }>REJECT</button>
                            <br></br>
                            { (singleLoan[ 6 ] !== "INTERVIEW PENDING") && (
                                <button onClick={ () =>
                                {
                                    setChooseInterviews(true);
                                    handleGrabInterviews();
                                    handleLoanAction(singleLoan[ 0 ], "INTERVIEW REQUIRED");
                                } }>INTERVIEW</button>
                            ) }
                            { singleLoan[ 6 ] === "INTERVIEW PENDING" && (
                                <button onClick={ () =>
                                {
                                    handleGrabInterviews();
                                    setChooseInterviews(true);

                                } }>
                                    SHOW INTERVIEW
                                </button>
                            ) }
                        </div>
                    ) }
                    { chooseInterviews && (
                        <div>
                            { singleLoan[ 6 ] !== "INTERVIEW PENDING" && (
                                <div>
                                    <h2>Choose Interview Slots</h2>
                                    <div className="home-features">
                                        <div className="feature-item">
                                            <input type="date" id="interview_day" name="interview_day" />
                                            <input type="time" id="interview_time" name="interview_time" />
                                            <button onClick={ () => handleAddInterview(singleLoan[ 0 ], document.getElementById("interview_day").value, document.getElementById("interview_time").value) }>Add Interview</button>
                                        </div>
                                    </div>
                                </div>
                            ) }
                            <h2>Interviews Slots</h2>
                            { interviews.map((interview) => (
                                <div className="home-features">
                                    <div className="feature-item">
                                        <div key={ interview[ 0 ] }>
                                            <p><strong>Day:</strong> { interview[ 3 ] }</p>
                                            <p><strong>Time:</strong> { new Date((parseFloat(interview[ 4 ])) * 1000).toISOString().slice(11, 16) }</p>
                                            { singleLoan[ 6 ] !== "INTERVIEW PENDING" && (
                                                <button onClick={ () => handleDeleteInterview(interview[ 0 ]) }>Remove</button>) }
                                        </div>
                                    </div>
                                </div>
                            )) }
                        </div>
                    ) }
                </div>
            </>
        )
    }

    // USER --------------------------------------

    const handleSlotSelect = (interviewId) =>
    {
        setSelectedSlot(interviewId === selectedSlot ? null : interviewId);
    };

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

    const handleChosenInterview = async () =>
    {
        try
        {
            alert("Updating interview slot, could take a while...");
            setInterviews([]);
            const response = await fetch(
                process.env.REACT_APP_API_URL + "/api/loan/interviews/chosen",
                {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ token: token, interview_id: selectedSlot, loan_id: singleLoan[ 0 ] }), // Assuming loan is an object with `id`
                }
            );
            const data = await response.json();
            if (data.confirm)
            {
                alert("Interview slot chosen successfully! Could take a while to reflect.");
                window.location.reload();
            } else
            {
                alert("Error choosing interview slot. Please try again later.");
            }
        } catch (error)
        {
            console.error("Error choosing interview slot:", error);
        }
    };

    const handleButtonClick = () =>
    {
        if (selectedSlot !== null)
        {
            handleChosenInterview();
        } else
        {
            alert("Please select an interview slot first.");
        }
    };

    const handlePay = async () =>
    {
        alert("Loan payment is being processed, could take a while...");
        try
        {
            const response = await fetch(
                process.env.REACT_APP_API_URL + "/api/loan/pay",
                {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ token: token, loan_id: singleLoan[ 0 ] }), // Assuming loan is an object with `id`
                }
            );
            const data = await response.json();
            if (data.message)
            {
                alert(data.message);
                window.location.href = "/";
            } else if (data.confirm)
            {
                alert("Loan paid successfully! Might take a few seconds to reflect.");
                window.location.reload();
            } else
            {
                alert("Error paying loan. Please try again later.");
            }
        } catch (error)
        {
            console.error("Error paying loan:", error);
        }
    };

    return (
        <>
            <Navbar />
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
                        ) }
                        <br></br>
                        { isLoggedIn && !hasLoans && !isSingleLoan && (
                            <button onClick={ handleLoanCheck }>Show Loan Applications</button>
                        ) }
                        { isLoggedIn && hasLoans && !isSingleLoan && (
                            <button onClick={ () =>
                            {
                                setHasLoans(false);
                                setLoans([]);
                                setInterviews([]);
                            } }>
                                Hide Loan Applications</button>
                        ) }
                        { isLoggedIn && isSingleLoan && (
                            <button onClick={ () =>
                            {
                                setIsSingleLoan(false);
                                setSingleLoan([]);
                            }
                            }>Hide Loan Details</button>
                        )
                        }

                        { isSingleLoan && singleLoan[ 6 ] === "ACCEPTED" && singleLoan[ 8 ] < (singleLoan[ 5 ] * singleLoan[ 4 ]) && (
                            <button className="btn btn-primary" onClick={ handlePay }>Pay</button>
                        ) }
                    </div>
                </div>
                { !hasLoans && (
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
                ) }
                { hasLoans && !isSingleLoan && (
                    <div className="home-features">
                        <h2>Your Loan Applications</h2>
                        <div className="features-grid">
                            { loans.map((loan, index) => (
                                <div className="feature-item"
                                    key={ index }
                                    onClick={ () =>
                                    {
                                        handleLoanClick(loan[ 0 ]);
                                    } }
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
                ) }
                { isSingleLoan && (
                    <div>
                        <h2>Loan ID: { singleLoan[ 0 ] }</h2>
                        <div className="home-features">
                            <div className="feature-item">
                                <p><strong>Status:</strong> { singleLoan[ 6 ] }</p>
                                <p>------</p>
                                <p><strong>Amount:</strong> ${ singleLoan[ 3 ] }</p>
                                <p><strong>Duration:</strong> { singleLoan[ 4 ] } months</p>
                                <p>------</p>
                                <p><strong>Monthly Payment:</strong> ${ singleLoan[ 5 ] }</p>
                                <p><strong>Total Paid:</strong> ${ singleLoan[ 8 ] }</p>
                                <p><strong>Total Payment:</strong> ${ singleLoan[ 5 ] * singleLoan[ 4 ] }</p>
                            </div>
                        </div>
                    </div>) }

                { isSingleLoan && singleLoan[ 6 ] === "INTERVIEW REQUIRED" && (
                    <button className="btn btn-primary" onClick={ handleGrabInterviews }>Grab Interviews</button>
                ) }

                { isSingleLoan && singleLoan[ 6 ] === "INTERVIEW PENDING" && (
                    <button className="btn btn-primary" onClick={ handleGrabInterviews }>Show Interview</button>
                ) }

                { isSingleLoan && interviews.length > 0 && singleLoan[ 6 ] === "INTERVIEW REQUIRED" && (
                    <div>
                        <h2>Interview</h2>
                        { interviews.map((interview) => (
                            <div className="home-features">
                                <div className="feature-item">
                                    <div key={ interview[ 0 ] }>
                                        <p><strong>Day:</strong> { interview[ 3 ] }</p>
                                        <p><strong>Time:</strong> { new Date((parseFloat(interview[ 4 ])) * 1000).toISOString().slice(11, 16) }</p>
                                        <button
                                            onClick={ () => handleSlotSelect(interview[ 0 ]) }
                                            style={ {
                                                backgroundColor: selectedSlot === interview[ 0 ] ? 'green' : 'lightgrey',
                                                color: 'white'
                                            } }
                                        >
                                            { selectedSlot === interview[ 0 ] ? 'Selected' : 'Select' }
                                        </button>
                                        <p>------</p>
                                    </div>
                                </div>
                            </div>
                        )) }
                        <button onClick={ handleButtonClick }>Confirm Selection</button>
                    </div>
                ) }

                { isSingleLoan && interviews.length > 0 && singleLoan[ 6 ] === "INTERVIEW PENDING" && (
                    <div>
                        <h2>Interviews</h2>
                        { interviews.map((interview) => (
                            <div className="home-features">
                                <div className="feature-item">
                                    <div key={ interview[ 0 ] }>
                                        <p><strong>Day:</strong> { interview[ 3 ] }</p>
                                        <p><strong>Time:</strong> { new Date((parseFloat(interview[ 4 ])) * 1000).toISOString().slice(11, 16) }</p>
                                    </div>
                                </div>
                            </div>
                        )) }
                    </div>
                ) }
            </div>
        </>
    );

};

export default Home;