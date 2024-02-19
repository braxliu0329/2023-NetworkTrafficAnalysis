import { ResponsiveBar } from '@nivo/bar'

interface FrequencyGraphProps {
    data: any[]
    index: string
};

const FrequencyGraph: React.FC<FrequencyGraphProps> = ({ data, index }) => {
    const getColor = (bar: any) => {
        const colorMap: { [key: string]: string} = {
            'TCP': '#003366',
            'UDP': '#006633',
            'UDP/DNS': '#006633',
            'IGMP': '#660066',
            'ICMP': '#006666',
            'ICMPv6': '#006666',
            'ARP': '#660000',
            'IPv6': '#666600'
        };
        if (colorMap.hasOwnProperty(bar.indexValue)) {
            return colorMap[bar.indexValue];
        }
        return '#e79a3f'
    }
    let legendOffsetY = -50;
    let marginL = 60;
    if (index === "source" || index === "dest" || index === "address") {
        legendOffsetY = -250;
        marginL = 300
    }
    if (index === "mac") {
        legendOffsetY = -150
        marginL = 155
    }
    let key = "frequency"
    let legend = "Frequency"
    if (index === "address") {
        key = "rate"
        legend = "SYN sending rate (packets/sec)"
    }
    return (
        <ResponsiveBar
            data={data}
            isInteractive={false}
            keys={[key]}
            indexBy={index}
            layout="horizontal"
            margin={{ top: 50, right: 130, bottom: 50, left: marginL }}
            padding={0.3}
            colors={getColor}
            borderColor={{ from: 'color', modifiers: [['darker', 1.6]] }}
            axisTop={null}
            axisRight={null}
            axisBottom={{
                legend: key,
                legendPosition: "middle",
                legendOffset: 36,
                tickSize: 5,
                tickPadding: 5,
                tickRotation: 0,
            }}
            axisLeft={{
                legend: index,
                legendPosition: "middle",
                legendOffset: legendOffsetY,
                tickSize: 5,
                tickPadding: 5,
                tickRotation: 0,
                
            }}
            labelSkipWidth={12}
            labelSkipHeight={12}
            labelTextColor={'white'}
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
            legends={index !== "source" && index != "dest" ? [
                {
                dataFrom: 'indexes',
                anchor: 'bottom-right',
                direction: 'column',
                justify: false,
                translateX: 120,
                translateY: 0,
                itemsSpacing: 2,
                itemWidth: 100,
                itemHeight: 20,
                itemDirection: 'left-to-right',
                itemOpacity: 0.85,
                itemTextColor: "white",
                symbolSize: 20,
                effects: [
                    {
                    on: 'hover',
                    style: {
                        itemOpacity: 1,
                    },
                    },
                ],
                },
            ] : []}
            animate={true}
    />
    );
}

export default FrequencyGraph;