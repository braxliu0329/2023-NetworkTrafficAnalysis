import FrequencyGraph from "../components/FrequencyGraph";
import data from "../../../../pythonGUI/plotData/protocols.json";

function ProtocolFrequencyAn() {
    return (
        <div className="Analysis">
            <h1>Protocol Frequency Analysis</h1>
            <div style={{height:400}}>
                <FrequencyGraph data={data}/>
            </div>
        </div>
    );
}

export default ProtocolFrequencyAn;