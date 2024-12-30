import React, { useCallback, useRef, useState } from "react";
import "./Login.css"; // Import the CSS file for styling
import Navbar from "../Navbar/Navbar";
import Webcam from 'react-webcam';

const Login = () =>
{
    const [ email, setEmail ] = useState("");
    const [ password, setPassword ] = useState("");
    const [ error, setError ] = useState(null);
    const [ loading, setLoading ] = useState(false);

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

    const handleLogin = async (e) =>
    {
        e.preventDefault();
        setLoading(true);
        setError(null);

        // Simulate login API request
        fetch(process.env.REACT_APP_API_URL + "/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password, photo: imgSrc }),
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
                if (data.username)
                {
                    alert(`Welcome, ${ data.username }!`);

                    const token = data.token;

                    localStorage.setItem("token", token);
                    localStorage.setItem("hasPermissions", data.hasPermissions);

                    setLoading(false);

                    window.location.href = "/"; // Redirect to home page
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
                    <form onSubmit={ handleLogin }>
                        <div className="form-group">
                            <label htmlFor="email">E-mail</label>
                            <input
                                type="text"
                                id="email"
                                value={ email }
                                onChange={ (e) => setEmail(e.target.value) }
                                required />
                        </div>
                        <div className="form-group">
                            <label htmlFor="password">Password</label>
                            <input
                                type="password"
                                id="password"
                                value={ password }
                                onChange={ (e) => setPassword(e.target.value) }
                                required />
                        </div>
                        <div className="container" style={ { width: '100%', height: '100%' } }>
                            { imgSrc ? (
                                <img src={ imgSrc } alt="webcam" style={ {
                                    maxWidth: '100%',
                                    maxHeight: '100%',
                                    objectFit: 'contain'
                                } } />
                            ) : (
                                    <Webcam screenshotFormat="image/jpeg" height="100%" width="100%" ref={ webcamRef } />
                            ) }
                            <div className="btn-container">
                                { imgSrc ? (
                                    <button type="button" onClick={ retake }>Retake photo</button>
                                ) : (
                                    <button type="button" onClick={ capture }>Capture photo</button>
                                ) }
                            </div>
                        </div>
                        { error && <p className="error-message">{ error }</p> }
                        <button type="submit" className="login-button" disabled={ loading }>
                            { loading ? "Logging in..." : "Login" }
                        </button>
                    </form>
                </div>
            </div></>
    );
};

export default Login;