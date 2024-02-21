import FrequencyGraph from "../components/FrequencyGraph";
import data from "../../../../pythonGUI/plotData/DestIP.json";
import { useState, useEffect } from 'react';

function DestFrequencyAn() {
    const [chartHeight, setChartHeight] = useState<number | string>('auto');

    useEffect(() => {
        const numEntries = data.length;
        let calculatedHeight = 400;
        if (numEntries > 5) {
            calculatedHeight = numEntries * 25;
        }
        setChartHeight(calculatedHeight);
    }, [data]);
    return (
        <div className="Analysis">
            <h1 className="title">Destination Frequency Analysis</h1>
            <div style={{height:chartHeight, width:1000}}>
                <FrequencyGraph data={data} index="dest"/>
            </div>
        </div>
    );
}

export default DestFrequencyAn;