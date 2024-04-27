This document is should assist any future teams working on Network Traffic Analysis. It contains information about how to use and develop on the program, some potential next steps if you're uncertain where to start, and any known issues that remain after this year's final release.

# Project Details
This project is split into two main programs:

 - A mostly Python-based packet capturing and analysis tool (`NTAnalyser`)
 - A Go project and executable that (very fundamentally) analyses `.pcap` files (`CLI Tool`)

NTAnalyser is the main focus of development, and has considerably more features, with the CLI Tool acting as a prototype in a faster-running language. All code can be found in the `src` directory.

## File Guide
*Less important files are grouped into their respective directories.*

| Filename          | Path       | Type                      | Usage                                                                                                                                                        |
|-------------------|------------|---------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `webguide`        | `docs`     | Directory (Documentation) | Contains an unused copy of the directory used to host and format the [usage guide webpage](https://tomossherlock.github.io/NetworkTrafficAnalysis/#/README). |
| `Handover.md`     | `docs`     | Documentation             | The handover guide for future teams' use (you're reading it)                                                                                                 |
| `MeetingNotes.md` | `Meetings` | Documentation             | Summary of group and client meetings, not important for future teams.                                                                                        |
| `Research`         | `~`        | Directory (Research)      | Contains attack analysis research and testing feedback.                                                                                                      |
| `                   |            |                           |                                                                                                                                                              |
