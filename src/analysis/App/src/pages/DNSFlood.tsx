import FrequencyGraph from "../components/FrequencyGraph";
import { useState, useEffect } from 'react';
import React from "react";

function DNSFlood() {
    const [resdata, setResData] = React.useState({} as any);
    const [reqdata, setReqData] = React.useState({} as any)
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
            const responseRes = await fetch('/api/dnsresdata');
            if (!responseRes.ok) {
                throw new Error('Failed to fetch data');
            }
            const resData = await responseRes.json();
            setResData(resData);
            const responseReq = await fetch('/api/dnsreqdata')
            if (!responseReq.ok) {
                throw new Error('Failed to fetch data')
            }
            const reqData = await responseReq.json()
            setReqData(reqData)
            // Calculate chart height based on number of nodes
            const numNodes = resData.nodes.length;
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
            <h1 className="title">DNS Flood Detection</h1>
            <div style={{ height: chartHeight, width:1000, margin: "auto" }}>
                <FrequencyGraph data={resdata.data} index={"address"}/>
            </div>
            <div style={{ height: chartHeight, width: 1000, margin: "auto" }}>
                <FrequencyGraph data={reqdata.data} index={"address"}/>
            </div>
            <div style={{ textAlign: "center", maxWidth: 600, margin: "auto" }}>
                <p><b>{resdata.suspicious}</b></p>
                <p>{resdata.explanation}</p>
            </div>
        </div>
    );
}

export default DNSFlood;