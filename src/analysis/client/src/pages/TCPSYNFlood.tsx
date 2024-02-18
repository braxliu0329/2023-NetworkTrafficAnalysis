import TCPFrequencyGraph from "../components/TCPFrequencyGraph";
import data from "../../../../pythonGUI/plotData/tcpsyn.json";

function TCPSYNFlood() {
    return (
        <div className="analysis">
            <h1 className="title">TCP SYN Flooding</h1>
            <div style={{ height: 400, width:1000, margin: "auto" }}>
                <TCPFrequencyGraph data={data.data}/>
            </div>
            <div style={{ textAlign: "center", maxWidth: 600, margin: "auto" }}>
                <p>{data.suspicious}</p>
                <p>{data.explanation}</p>
            </div>
        </div>
    );
}

export default TCPSYNFlood;