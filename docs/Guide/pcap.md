# Packet Capturing
The packet capturing feature of the network traffic analysis tool is implemented through the main GUI. No arguments need to be specified to capture packets.

## Capture Control
![image](https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/03724170-9fd2-44ba-9972-175eba58a39c)

To begin capturing packets that pass through your device, press the `start capture` button. 
 - <img src="https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/90357e34-4289-4167-b24b-0acad21284f9" alt="play button" style="width:1em;"/>    Start/Resume packet capturing on the network
 - <img src="https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/2d96d5c3-5136-468b-80ce-044f646e1f83" alt="pause button" style="width:1em;"/> Pause packet capturing. Will not clear current packets.
 - <img src="https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/11a144a4-11cc-4546-9fd4-8f911ce06d40" alt="stop button" style="width:1em;"/> Stop packet capturing. *Will clear all captured packets*.
 - <img src="https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/09f9e042-e1e3-45ea-9489-a85766beffba" alt="magnifying glass button" style="width:1em;"/> Start Analysis. Analysis will run in the background. More detail provided in the Analysis Guide.

## File Management and Configuration
![image](https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/f0975779-d0cd-4c67-b7f4-78827f6987ff)



All currently captured packets can be saved as a `.pcap` file. Any accessible `.pcap` files can be opened using the `open file` button or `CTRL+O`. Multiple files can be opened at once using `CTRL+SHIFT+O`.
 - <img src="https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/81c5bc22-9fa4-4d2e-b49e-597e13a40821" alt="save button" style="width:1em;"/> Save captured packets. Will bring up the standard file saving window. `CTRL+S`
 - <img src="https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/89a65b8d-2b0c-4256-b7f9-00bf4976c3f5" alt="load file button" style="width:1em;"/> Load a `.pcap` file. Will bring up standard file loading window. `CTRL+O`
 - <img src="https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/d1905a50-8cf9-4908-975c-67988a7a6383" alt="settings button" style="width:1em;"/> Bring up configuration window:

<img src="https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/7062a585-d126-4519-8e2b-50e45a6016d5" alt="settings button" align="left" style="padding-right:30px"/>
<br>
<br>
<br>
Here, the threshold settings of attack analyses can be changed. Any changed thresholds will overwrite the default thresholds and get saved to a config file. The application of these thresholds is explained in the Analysis Guide.
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br><br>
<br>

## Packet Selection

![image](https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/1918486b-5749-4ba7-8996-465bacdf8a47)

Packets can be selected using the selection buttons or by left-clicking. By holding control, mutiple packets can be selected or deselected at once. Selected packets can be marked/unmarked using `CTRL+M` or the edit toolbar (marked packets will be highlighted black). Selected packets can be ignored/unignored using `CTRL+D`. Ignored packets will be highlighted black, and will not be analysed. All packets can be ignored with `CTRL+SHIFT+D`.

 - <img src="https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/e9f439d2-dc9e-444e-898f-e779486866fa" alt="left button" style="width:1em;"/> Select the previous packet. Selects the latest packet if no packets are selected.
 - <img src="https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/de8ae097-fc3b-4b3c-9e81-2a46c22fc5ac" alt="right button" style="width:1em;"/> Select the next packet. Selects the first packet if no packets are selected.
 - By double-clicking on a packet, the following window containing raw packet data and layer details apppears:
![image](https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/a52e0b21-9c7a-4b7e-ae1b-1530b76236a9)

## Packet Filtering
![image](https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/2b22c083-5400-44b2-9dc0-338641d844b2)
Packets can be filtered using the filter inputs. Once the filter button is pressed, any packets not matching the specified filters will be removed, and no future packets outside the filter will show up.

-  *Protocol*: Select a protocol to filter packets by.
-  *Source Address*: Enter the source address that all packets must come from.
-  *Destination Address*: Enter the address all packets must have as their destination.
-  <img src="https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/3788e3fa-e9ad-4142-a0b3-462dbadd5840" alt="filter button" style="width:3em;"/> Apply the specified filter to current and future packets.
-  *Amount*: Limit the maximum number of packets captured. Needs to be specified before capture. Once specified, any packets past the specified limit will not show up.

