import React from "react";
import FrequencyGraph from "../components/FrequencyGraph";
import { useState, useEffect } from 'react';

function HTTPFlood() {
    const [data, setData] = React.useState({} as any);
    const [chartHeight, setChartHeight] = useState<number | string>('auto');

    // Fetch data from the backend when the component mounts
    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 5000)
        return () => clearInterval(interval)
       
    }, []);

    // Fetch data from the backend
    const fetchData = async () => {
        try {
            const response = await fetch('/api/httpflooddata');
            if (!response.ok) {
                throw new Error('Failed to fetch data');
            }
            const jsonData = await response.json();
            setData(jsonData);

            // Calculate chart height based on number of Entries
            const numEntries = jsonData.data.length;
            let calculatedHeight = 400;
            if (numEntries > 5) {
                calculatedHeight = numEntries * 25;
            }
            setChartHeight(calculatedHeight);
        } catch (error) {
            console.error(error);
        }
    };
    return (
        <div className="analysis">
            <h1 className="title">HTTP Flood Detection</h1>
            <div style={{ height: chartHeight, width:1000, margin: "auto" }}>
                <FrequencyGraph data={data.data} index={"address"}/>
            </div>
            <div style={{ textAlign: "center", maxWidth: 600, margin: "auto" }}>
                <p><b>{data.suspicious}</b></p>
                <p>{data.explanation}</p>
            </div>
        </div>
    );
}

export default HTTPFlood;