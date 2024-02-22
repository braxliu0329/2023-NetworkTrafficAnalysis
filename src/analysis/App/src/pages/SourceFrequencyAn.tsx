import FrequencyGraph from "../components/FrequencyGraph";
import data from "../../../../pythonGUI/plotData/SourceIP.json";
import { useState, useEffect } from 'react';

function SourceFrequencyAn() {
    const [chartHeight, setChartHeight] = useState<number | string>('auto');
    // Sets heights based on number of addresses
    useEffect(() => {
        const numEntries = data.length;
        let calculatedHeight = 400;
        if (numEntries > 20) {
            calculatedHeight = numEntries * 20;
        }
        setChartHeight(calculatedHeight);
    }, [data]);
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