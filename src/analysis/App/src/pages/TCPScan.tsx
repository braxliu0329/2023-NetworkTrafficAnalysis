import data from "../../../../pythonGUI/plotData/tcpscan.json";
import FrequencyGraph from "../components/FrequencyGraph";
import { useState, useEffect } from 'react';

function TCPScan() {
    const [chartHeight, setChartHeight] = useState<number | string>('auto');

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
            <h1 className="title">TCP Connect Scanning</h1>
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

export default TCPScan;