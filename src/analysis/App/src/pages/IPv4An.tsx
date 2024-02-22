import NetworkGraph from '../components/NetworkGraph'
import data from '../../../../pythonGUI/plotData/ipv4.json'
import { useEffect, useState } from 'react';

function IPv4An() {
    const [chartHeight, setChartHeight] = useState<number | string>('auto');

    useEffect(() => {
        const numNodes = data.nodes.length;
        const calculatedHeight = numNodes * 30; 
        setChartHeight(calculatedHeight);
    }, [data]);
    return (
        <div className="Analysis">
            <h1 className="title">IPv4 Analysis</h1>
            <div className='description'>
                <p>This is a visualisation of different IPv4 nodes. Every node is a different address.</p>
                <p>Every edge between a node means that these two addresses have communicated with each other.</p>
                <p>These graphs are undirected, so it is not indicated whether a node is the receiver, sender, or both.</p>
                <p>Hovering over a node will display its address. A link is indicative of if a connection between these 
                addresses has been made, not the number of times they have communicated.
                </p>
                <p>These graphs can grow quite large, so scrolling may be needed. It is usual for an IPv4 graph to be
                more dense than its IPv6 counterpart, though this is not always the case.
                </p>
            </div>
            <div style={{height:chartHeight}}>
                <NetworkGraph data={data}/>
            </div>
        </div>
    );
}

export default IPv4An;