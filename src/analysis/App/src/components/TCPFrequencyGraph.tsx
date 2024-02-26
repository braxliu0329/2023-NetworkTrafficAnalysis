import { ResponsiveBar } from "@nivo/bar";

interface BarData {
    address: string;
    sendsSYN: number;
    receivesSYN: number;
    sendSYNACK: number;
    receivesSYNACK: number;
}

interface BarGraphProps {
    data: BarData[];
}

// The TCP/SYN attack is visualised using a unique grouped data bar chart,
// so it's best to have it in a separate component
const TCPFrequencyGraph: React.FC<BarGraphProps> = ({ data }) => {
    // Formats the JSON fields to be readable
    const formattedData = data.map(item => ({
        address: item.address,
        'Sends SYN': item.sendsSYN,
        'Receives SYN': item.receivesSYN,
        'Send SYN/ACK': item.sendSYNACK,
        'Receives SYN/ACK': item.receivesSYNACK,
    }));

    return (
            <ResponsiveBar
                data={formattedData}
                isInteractive={false}
                keys={['Sends SYN', 'Receives SYN', 'Send SYN/ACK', 'Receives SYN/ACK']}
                indexBy="address"
                margin={{ top: 50, right: 160, bottom: 50, left: 150 }}
                padding={0.3}
                layout="horizontal"
                colors={{ scheme: 'nivo' }}
                labelSkipWidth={12}
                labelSkipHeight={12}
                labelTextColor={{ from: 'color', modifiers: [['darker', 1.6]] }}
                axisBottom={{
                    legend: "Frequency",
                    legendPosition: "middle",
                    legendOffset: 36,
                    tickSize: 5,
                    tickPadding: 5,
                    tickRotation: 0,
                }}
                axisLeft={{
                    legend: "Address",
                    legendPosition: "middle",
                    legendOffset: -100,
                    tickSize: 5,
                    tickPadding: 5,
                    tickRotation: 0,
                    
                }}
                legends={[
                    {
                        dataFrom: 'keys',
                        anchor: 'bottom-right',
                        direction: 'column',
                        justify: false,
                        translateX: 120,
                        translateY: 0,
                        itemsSpacing: 2,
                        itemWidth: 100,
                        itemHeight: 20,
                        itemDirection: 'left-to-right',
                        itemTextColor: 'white',
                        symbolSize: 20,
                    },
                ]}
                
                theme={{
                    axis:{
                        ticks: {
                            text: {
                                fill: "#c79eba"
                            }
                        },
                        legend: {
                            text:{
                                fill: "#ab6d98"
                            }
                        }
                    }
                }}
                animate={true}
            />
    );
};

export default TCPFrequencyGraph;