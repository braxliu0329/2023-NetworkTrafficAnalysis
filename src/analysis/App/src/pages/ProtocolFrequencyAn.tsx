import FrequencyGraph from "../components/FrequencyGraph";
import { useEffect, useState } from "react";

interface ProtocolData {
    protocol: string;
    frequency: number;
  }
  

function ProtocolFrequencyAn() {
    const [data, setData] = useState<ProtocolData[]>([]);

    // Fetch data from the backend when the component mounts
    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 5000)
        return () => clearInterval(interval)
       
    }, []);

    // Fetch data from the backend
    const fetchData = async () => {
        try {
            const response = await fetch('/api/protocoldata');
            if (!response.ok) {
                throw new Error('Failed to fetch data');
            }
            const jsonData = await response.json();
            
            setData(jsonData.data);
            
        } catch (error) {
            console.error(error);
        }
    };
    return (
        <div className="analysis">
            <h1 className="title">Protocol Frequency Analysis</h1>
            <div style={{ height: 400, width: 1000, alignSelf: "center" }}>
                <FrequencyGraph data={data} index="protocol"/>
            </div>
        </div>
    );
}

export default ProtocolFrequencyAn;