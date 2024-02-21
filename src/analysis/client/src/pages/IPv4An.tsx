import NetworkGraph from '../components/NetworkGraph'
import data from '../../../../pythonGUI/plotData/ipv4.json'
import { useEffect, useState } from 'react';

function IPv4An() {
    const [chartHeight, setChartHeight] = useState<number | string>('auto');

    useEffect(() => {
        const numNodes = data.nodes.length;
        const calculatedHeight = numNodes * 50 + 200; 
        setChartHeight(calculatedHeight);
    }, [data]);
    return (
        <div className="Analysis">
            <h1>IPv4 Analysis</h1>
            <div style={{height:chartHeight}}>
                <NetworkGraph data={data}/>
            </div>
        </div>
    );
}

export default IPv4An;