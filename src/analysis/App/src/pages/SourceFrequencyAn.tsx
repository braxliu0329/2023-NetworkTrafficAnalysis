import FrequencyGraph from "../components/FrequencyGraph";
import data from "../../../../pythonGUI/plotData/SourceIP.json";
import { useState, useEffect } from 'react';

function SourceFrequencyAn() {
    const [chartHeight, setChartHeight] = useState<number | string>('auto');

    useEffect(() => {
        const numNodes = data.length;
        const calculatedHeight = numNodes * 20; 
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