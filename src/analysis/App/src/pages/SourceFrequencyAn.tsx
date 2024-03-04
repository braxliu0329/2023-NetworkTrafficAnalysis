import FrequencyGraph from "../components/FrequencyGraph";
import React from "react";
import { useState, useEffect } from 'react';

function SourceFrequencyAn() {
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
            const response = await fetch('/api/sourcedata');
            if (!response.ok) {
                throw new Error('Failed to fetch data');
            }
            const jsonData = await response.json();
            setData(jsonData);

            // Calculate chart height based on number of nodes
            const numNodes = jsonData.nodes.length;
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
        <div className="Analysis">
            <h1 className="title">Source Frequency Analysis</h1>
            <div style={{height:chartHeight, width:1000}}>
                <FrequencyGraph data={data} index="source"/>
            </div>
        </div>
    );
}

export default SourceFrequencyAn;