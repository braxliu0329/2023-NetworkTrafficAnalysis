import NetworkGraph from '../components/NetworkGraph'
import data from '../../../../pythonGUI/plotData/mac.json'
import { useState, useEffect } from 'react';

function MACAn() {
    const [chartHeight, setChartHeight] = useState<number | string>('auto');
    // Sets heights based on number of nodes in network
    useEffect(() => {
        const numNodes = data.nodes.length;
        const calculatedHeight = numNodes * 50; 
        setChartHeight(calculatedHeight);
    }, [data]);
    return (
        <div className="Analysis">
            <h1 className="title">MAC Analysis</h1>
            <div className="description">
                <p>This is a visualisation of different MAC nodes. Every node is a different address.</p>
                <p>Every edge between a node means that these two addresses have communicated with each other.</p>
                <p>These graphs are undirected, so it is not indicated whether a node is the receiver, sender, or both.</p>
                <p>Hovering over a node will display its address. A link is indicative of if a connection between these 
                addresses has been made, not the number of times they have communicated.
                </p>
                <p>These graphs can grow quite large, so scrolling may be needed. A MAC graph is generally more sparse 
                than an IPv6 or IPv4, since network interfaces may have multiple IPs, but will have only one MAC address.
                </p>
            </div>
            <div style={{height:chartHeight}}>
                <NetworkGraph data={data}/>
            </div>
        </div>
    );
}

export default MACAn;