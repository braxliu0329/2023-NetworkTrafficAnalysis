import FrequencyGraph from "../components/FrequencyGraph";
import data from "../../../../pythonGUI/plotData/arp.json";

function ArpPoision() {
    return (
        <div className="analysis">
            <h1 className="title">Arp Poisoning</h1>
            <div style={{ height: 400, width: 1000, alignSelf: "center" }}>
                <FrequencyGraph data={data.data} index="mac"/>
            </div>
            <div>
                <p>{data.suspicious}</p>
                <p>{data.explanation}</p>
            </div>
        </div>
    );
}

export default ArpPoision;