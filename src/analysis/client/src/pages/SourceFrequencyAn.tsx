import FrequencyGraph from "../components/FrequencyGraph";
import data from "../../../../pythonGUI/plotData/SourceIP.json";

function SourceFrequencyAn() {
    return (
        <div className="Analysis">
            <h1 className="title">Source Frequency Analysis</h1>
            <div style={{height:400, width:1000}}>
                <FrequencyGraph data={data} index="source"/>
            </div>
        </div>
    );
}

export default SourceFrequencyAn;