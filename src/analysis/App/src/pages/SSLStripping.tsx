import FrequencyGraph from "../components/FrequencyGraph";
import { useState, useEffect } from 'react';
import React from "react";

function SSLStripping() {
    const [sourcedata, setSourceData] = React.useState({} as any);
    const [destdata, setDestData] = React.useState({} as any)
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
            const responseSource = await fetch('/api/sslsourcedata');
            if (!responseSource.ok) {
                throw new Error('Failed to fetch data');
            }
            const sourceData = await responseSource.json();
            setSourceData(sourceData);
            const responseDest = await fetch('/api/ssldestdata')
            if (!responseDest.ok) {
                throw new Error('Failed to fetch data')
            }
            const destData = await responseDest.json()
            setDestData(destData)
            // Calculate chart height based on number of nodes
            const numNodes = destData.data.length;
            let calculatedHeight = 400;
            if (numNodes > 20) {
                calculatedHeight = numNodes * 20;
            }
            setChartHeight(calculatedHeight);
        } catch (error) {
            console.error(error);
        }
    };
    return (
        <div className="analysis">
            <h1 className="title">SSL Stripping Detection</h1>
            <div style={{ height: chartHeight, width:1000, margin: "auto" }}>
                <FrequencyGraph data={sourcedata.data} index={"ssl"}/>
            </div>
            <div style={{ height: chartHeight, width: 1000, margin: "auto" }}>
                <FrequencyGraph data={destdata.data} index={"ssl"}/>
            </div>
            <div style={{ textAlign: "center", maxWidth: 600, margin: "auto" }}>
                <p><b>{sourcedata.suspicious}</b></p>
                <p>{sourcedata.explanation}</p>
            </div>
        </div>
    );
}

export default SSLStripping;