import NetworkGraph from '../components/NetworkGraph'
import data from './ipv4.json'

function IPv4An() {
    return (
        <div className="Analysis">
            <h1>IPv4 Analysis</h1>
            <div style={{height:400}}>
                <NetworkGraph data={data}/>
            </div>
        </div>
    );
}

export default IPv4An;