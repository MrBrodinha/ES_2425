import React, { useEffect, useState } from "react";

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
        <div>
            {loading ? "Loading..." : data}
        </div>
    );
}

export default Home;