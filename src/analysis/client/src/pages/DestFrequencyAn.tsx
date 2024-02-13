import FrequencyGraph from "../components/FrequencyGraph";
import data from "../../../../pythonGUI/plotData/DestIP.json";

function DestFrequencyAn() {
    return (
        <div className="Analysis">
            <h1 className="title">Destination Frequency Analysis</h1>
            <div style={{height:400, width:1000}}>
                <FrequencyGraph data={data} index="dest"/>
            </div>
        </div>
    );
}

export default DestFrequencyAn;