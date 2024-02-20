import data from "../../../../pythonGUI/plotData/httpflood.json";
import FrequencyGraph from "../components/FrequencyGraph";

function HTTPFlood() {
    return (
        <div className="analysis">
            <h1 className="title">HTTP Flood Detection</h1>
            <div style={{ height: 400, width:1000, margin: "auto" }}>
                <FrequencyGraph data={data.data} index={"address"}/>
            </div>
            <div style={{ textAlign: "center", maxWidth: 600, margin: "auto" }}>
                <p><b>{data.suspicious}</b></p>
                <p>{data.explanation}</p>
            </div>
        </div>
    );
}

export default HTTPFlood;