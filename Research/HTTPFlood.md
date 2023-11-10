# HTTP Flood:
An HTTP Flood is a type of Distributed Denial of Service (DDoS) attack where an attacker exploits seemingly legitimate HTTP GET or POST requests to attack a web server or application.

  - ## Outline
    HTTP Flood attacks are volumetric in nature, aiming to overwhelm the target with a flood of TCP connections or HTTP requests,
     ultimately exhausting the server's resources and bandwidth. Unlike other forms of DDoS attacks that use malformed packets or low-level network protocols,
     HTTP Floods utilize valid requests to the same resource, such as a URL or API endpoint.
  
  - ## Methods of Preventing HTTP Flood:
  
    - ### Web Application Firewalls (WAFs):
      To inspect incoming traffic and block suspicious activity.
    - ### Rate Limiting:
      To control the number of requests a user can make in a certain time frame.
    - ### Challenge-Response Tests:
      Such as CAPTCHAs, to differentiate between bots and humans.

