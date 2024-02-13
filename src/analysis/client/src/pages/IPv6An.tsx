import NetworkGraph from '../components/NetworkGraph'
import data from '../../../../pythonGUI/plotData/ipv6.json'

function IPv6An() {
    return (
        <div className="Analysis">
            <h1>IPv6 Analysis</h1>
            <div style={{height:400}}>
                <NetworkGraph data={data}/>
            </div>
        </div>
    );
}

export default IPv6An;