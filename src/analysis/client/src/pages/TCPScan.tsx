import data from "../../../../pythonGUI/plotData/tcpscan.json";
import FrequencyGraph from "../components/FrequencyGraph";

function TCPScan() {
    return (
        <div className="analysis">
            <h1 className="title">TCP Connect Scanning</h1>
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

export default TCPScan;