import TCPFrequencyGraph from "../components/TCPFrequencyGraph";
import data from "../../../../pythonGUI/plotData/tcpsyn.json";
import { useState, useEffect } from 'react';

function TCPSYNFlood() {
    const [chartHeight, setChartHeight] = useState<number | string>('auto');
    // Sets heights based on number of addresses
    useEffect(() => {
        const numEntries = data.data.length;
        let calculatedHeight = 400;
        if (numEntries > 20) {
            calculatedHeight = numEntries * 25;
        }
        setChartHeight(calculatedHeight);
    }, [data]);
    return (
        <div className="analysis">
            <h1 className="title">TCP SYN Flooding</h1>
            <div style={{ height: chartHeight, width:1000, margin: "auto" }}>
                <TCPFrequencyGraph data={data.data}/>
            </div>
            <div style={{ textAlign: "center", maxWidth: 600, margin: "auto" }}>
                <p><b>{data.suspicious}</b></p>
                <p>{data.explanation}</p>
            </div>
        </div>
    );
}

export default TCPSYNFlood;