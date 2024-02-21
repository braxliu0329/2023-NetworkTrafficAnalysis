import NetworkGraph from '../components/NetworkGraph'
import data from '../../../../pythonGUI/plotData/ipv6.json'
import { useEffect, useState } from 'react';

function IPv6An() {
    const [chartHeight, setChartHeight] = useState<number | string>('auto');

    useEffect(() => {
        const numNodes = data.nodes.length;
        const calculatedHeight = numNodes * 20; 
        setChartHeight(calculatedHeight);
    }, [data]);
    return (
        <div className="Analysis">
            <h1 className='title'>IPv6 Analysis</h1>
            <div style={{height:chartHeight, width:chartHeight}}>
                <NetworkGraph data={data}/>
            </div>
        </div>
    );
}

export default IPv6An;