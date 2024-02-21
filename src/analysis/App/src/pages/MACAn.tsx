import NetworkGraph from '../components/NetworkGraph'
import data from '../../../../pythonGUI/plotData/mac.json'
import { useState, useEffect } from 'react';

function MACAn() {
    const [chartHeight, setChartHeight] = useState<number | string>('auto');

    useEffect(() => {
        const numNodes = data.nodes.length;
        const calculatedHeight = numNodes * 20; 
        setChartHeight(calculatedHeight);
    }, [data]);
    return (
        <div className="Analysis">
            <h1 className="title">MAC Analysis</h1>
            <div style={{height:chartHeight, width:chartHeight}}>
                <NetworkGraph data={data}/>
            </div>
        </div>
    );
}

export default MACAn;