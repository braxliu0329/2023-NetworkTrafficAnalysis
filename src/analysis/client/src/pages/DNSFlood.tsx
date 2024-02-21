import resdata from "../../../../pythonGUI/plotData/dnsresponse.json";
import reqdata from "../../../../pythonGUI/plotData/dnsrequest.json"
import FrequencyGraph from "../components/FrequencyGraph";

function DNSFlood() {
    return (
        <div className="analysis">
            <h1 className="title">DNS Flood Detection</h1>
            <div style={{ height: 400, width:1000, margin: "auto" }}>
                <FrequencyGraph data={resdata.data} index={"address"}/>
            </div>
            <div style={{ height: 400, width: 1000, margin: "auto" }}>
                <FrequencyGraph data={reqdata.data} index={"address"}/>
            </div>
            <div style={{ textAlign: "center", maxWidth: 600, margin: "auto" }}>
                <p><b>{resdata.suspicious}</b></p>
                <p>{resdata.explanation}</p>
            </div>
        </div>
    );
}

export default DNSFlood;