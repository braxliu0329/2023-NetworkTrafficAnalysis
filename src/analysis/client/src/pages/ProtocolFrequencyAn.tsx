import FrequencyGraph from "../components/FrequencyGraph";
import data from "../../../../pythonGUI/plotData/Protocol.json";

function ProtocolFrequencyAn() {
    return (
        <div className="analysis">
            <h1 className="title">Protocol Frequency Analysis</h1>
            <div style={{ height: 400, width: 1000, alignSelf: "center" }}>
                {/* Assuming FrequencyGraph is properly implemented */}
                <FrequencyGraph data={data} index="protocol"/>
            </div>
        </div>
    );
}

export default ProtocolFrequencyAn;