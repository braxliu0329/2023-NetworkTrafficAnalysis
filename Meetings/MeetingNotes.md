## Group Mentor Meeting 10/10/2023 ##
Group Members Present: Ani, Tomos, Tony, Joe  
Others Present: Oliver (Mentor)
- Group roles were discussed:
  - Client Liaison - Ani
  - Admin and Notes - Tomos
- Oliver suggested Kanban board improvements:
  - Add labels to all issues
  - Implement issue templates
  - Add descriptions to all issues
  - Ensure each team member always has a task in progress
- Ani has emailed with the provided client contact
  - This contact has referred us to another client
  - The client has been contacted by the contact and should contact us to arrange a meeting
  - The client has not yet contacted us
  - Ani has sent another email to the client to ensure they are working towards a meeting
- Oliver provided tips for github:
  - Each group member should be working on roughly one branch each
  - Branches should be named after the work, not after the group member adding to it
  - Ensuring the github is tidy before starting new work is vital
- Oliver also provided other important information:
  - Starting next week, public rankings will be used to store team progress
  - There should be no difficult ethical considerations for our project
  - Client meetings are likely to happen over zoom
  - It is important to have a stable release to show to the client each meeting
- Next steps were discussed:
  - Familiarise ourselves with the files that we will be working on
  - Research the technologies brought up by the client
  - Consider the feasibility of changing the project's language from python

## Client Meeting 17/10/2023 ##
Group Members Present: Ani, Tomos, Tony, Joe  
Others Present: Louis (Client)
- The general project outcome was discussed:
  - We will be improving last year's existing solution
    - The existing solution was implemented in Python
  - Improving the project's documentation and comments was requested, and will help us better understand the project
  - Adding detection of more methods of cyberattacks would serve as a good stretch goal
  - Last year's project's GUI needs improvement
- The feasibility of implementing code via a different programming language than Python was discussed:
  - Python is often considered slow and unoptimised
  - Critical sections of code can be rewritten in a better optimised language
  - Adding a new language would require implementation of a new compatibility layer
  - Ani suggests Golang as the new language
    - Golang is part of the CS course, so we should be familiar with it
    - Golang is optimised well, similarly to languages such as C
    - Golang allows specific parallelization implementation to further optimise
- Minimum Viable Product requirements were discussed:
  - The MVP should have at least the same functionality as the original solution
  - Another fleshed out feature would be good
  - Comments on last year's code
- Ani asked Louis about Stakeholders and User Stories:
  - The tool will be used by Synoptix
  - It will likely be used by people in IT who are experienced with cybersecurity
  - Louis will send a follow-up email with more detailed user stories
- Legal and Ethical issues were discussed:
  - A legal contract was made and signed last year
  - Louis will forward the desired contract
  - There is no reason to worry about ethical considerations, as no personal data is used

## Group Mentor Meeting 25/10/2023 ##
Group Members Present: Ani, Tomos  
Group Members Absent: Tony, Joe  
Others Present: Oliver (Mentor)  
- This week's group rankings and feedback were evaluated:
  - Our project was ranked 12th
  - The ReadMe was the main area to be improved
    - Every section should be filled in soon
    - Last year's project ReadMe can be used as inspiration
  - Branch names should be in dash camel case and more concise
  - The development branch should be renamed to dev to allow easier access for markers
  - There is no need to allocate everyone to an issue, allocate no one instead
- Oliver also gave some more specific feedback:
  - Make milestones to group issues
  - Split up larger issues such as "comment code"
  - Don't risk changing any code while commenting - it could break everything!
  - When considering someone else's code related pull request, make sure it runs on your machine
  - It would be a good idea to make a commit to main with a good ReadMe and the code
- Tomos suggested setting up branch protection on github
  - Only the mentor (Oliver) can change the repo settings
  - The group decided on the following branch rules:
    - dev and main both require pull requests to commit and merge branches
    - Pull requests need to be approved by one other team member before pulling to dev
    - Pull requests need to be approved by two other team members before pulling to main
- The contract was discussed:
  - The soft deadline for submitting the contract is 25/10/2023
  - Ani has not yet received any updates from the client about which contract to go for
  - Every group member will need to sign the contract, and the client will need to sign the contract before submitting it
  - Ani will send a follow up email to the client about the contract
 
 ## Group Mentor Meeting 8/11/2023
 Group Members Present: Ani, Tomos, Tony, Joe    
 Others Present: Oliver (Mentor)
### Rankings and Feedback
 - Oliver had not yet recieved our group's rankings for last week
 - Oliver suggests, given the volatility of the top ten rankings, staying within the top ten is an impressive feat to go for
 - Ideally, everyone should be working on one issue and on one seperate branch at all times
 - Team members should commit to branches consistently
### Progress
 - Tomos has overhauled the repo's organisation
   - A Gantt Chart has been added as a view to the kanban board, with the completion dates of issues noted
   - The Readme has been updated with stakeholders and deployment instructions
   - A docs directory has been added to the repo
   - Pull request and issue templates have been added to the new docs folder to allow better documentation and realisation of next steps
- Ani has been researching how to best update the GUI
- Joe has completed the ethics form
- Tony has added some user stories to the Readme
### Next Steps
 - This week's weekly workbooks are on cloud computing, which is not applicable to our project
 - Tomos, Tony and Joe will begin commenting different files of the code
 - Ani will continue to research and update the GUI

## Group Mentor Meeting 24/01/2024
Group Members Present: Tomos, Tony, Joe
Others Present: Oliver (Mentor)
### Rankings and Feedback
 - Many groups have done work over the holidays, so the rankings have dropped from 4th
 - The group's average score has dropped to 0.7
 - All issues need branches - even if empty?
 - They want the user stories to follow the format "as a _, I want to _, because _ "
 - We should look into Continuous Deployment
### Progress
 - Ani has set up a meeting with the client for next Wednesday
 - The email issue has been resolved
 - Continuous integration has been set up
 - We have decided to go with Go for the CLI implementation
### Next Steps
 - Tomos will work on an action plan for TB2
 - Joe will finish adding install instructions for pcap and look into a new attack 
 - Tony will continue looking into new attack methods
 - Ani will continue working on the GUI

## Client Meeting 31/01/2024 ##
Group Members Present: Tomos, Tony, Joe  
Others Present: Louis Goodland (Client)
### The Minimum Viable Product
  - The current state of the new GUI was showcased
  - The documentation of the code was displayed
### Client Communication
  - The next meeting was provisionally scheduled for Wednesday 14th 12:00
  - Weekly update emails will be sent to the client
### Next Steps
  - Tomos will start work on the GO CLI implementation
  - Joe and Tony will add new attack method analyses
  - Ani will polish and finish the GUI

## Group Mentor Meeting 07/02/2024
 Group Members Present: Ani, Tomos, Tony
 Others Present: Oliver (Mentor)
### Rankings and Feedback
 - Rankings have gone up - we are currently 10th
 - The Readme structure can be changed - only one bullet point per user
### Progress
 - Tomos has begun working on the GO CLI Implementation
 - Ani is working on the final aspects of the GUI
 - Tony has implemented a new attack analysis method
### Next Steps
 - An email will be sent to the client updating him on this week's progress
 - Ani will finish up the GUI
 - Tony and Joe will continue adding more attack analyses
 - Tomos will look into setting up continuous development

## Client Meeting 14/02/2024
Group Members Present: Tomos, Ani, Tony
Group Members Absent: Joe
Others Present: Louis Goodland (Client)
### Progress
 - Ani has continued work on the GUI - to fix and improve the graphs from the existing GUI, a local react page has been made to dynamically display attack analyses.
 - Tony has worked on developing new attack detection methods - UDP Flood detection and SSL Stripping
 - Joe has been working on DNS amplification detection
### Feedback
 - The CLI analysis tool should be more of a "packet disector" than a packet analysis tool
 - GUI feedback:
 ![image](https://github.com/spe-uob/2023-NetworkTrafficAnalysis/assets/123552121/0738a737-a676-4c8a-8234-dd580618fa14)
### Next Steps
 - Tomos will continue working on the CLI implementation in Go
 - Ani will continue working on the react side of the GUI
 - Tony will continue implementing attack detections

## Group Meeting 21/02/2024
Group Members Present: Tomos, Tony
Group Members Absent: Ani, Joe
### Progress
 - Tomos has implemented the attack analysis methods in Go
 - Tony has implemented SSL stripping
### Testing Feedback
 - During testing day, consensus was split about having the attack analysis window embedded within the program or on a webopage separately
 - Some result say the GUI is unintiutive
 - On some laptops, the important stop and start buttons are too small
 - Other feedback will be collated
 - The new graphs could be hard to follow, and might need a redesign
### Next Steps
 - Tony will work on the analysis window for all of the new attack analyses
 - Tomos will collate all the research, along with working on Main for the Go implementation

## Mentor and Group Meeting 06/03/2024
Group Members Present: Tomos, Ani, Tony
Group Members Absent: Joe
### Progress
 - Ani has integrated the react page for the attack analyses
   - This will require assistance to pass the continuous integration
 - Tomos has finished work on the basic GO CLI implementation
 - Tony has implemented the analysis window for UDP flood analysis
### Weekly Feedback
 - A lot of scores are max
 - Pull request names could be more descriptive
 - Run more tests in CI - test that the setup works, split tests into smaller tests
### Next Steps
 - Tomos will update the CI this week, and ensure the functionality of the CLI tool
 - Ani will complete the GUI to the Beta standard
 - Tony will integrate the analysis windows for all remaining tests
