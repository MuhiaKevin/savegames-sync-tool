# savegames-sync-tool

A tool to upload my save games to Google Drive


### Future improvements
- check if the directory exists
- if folder exists check if it is saved in the database
- if folder exists and is in the database, calculate the sha256 and check if it the same as that in the sqlite database
- if it has changed then upload to cloud
- if it has not changed then leave it as it is
- if folder does not exist then throw error

### Future improvements
These are some of the additional features i plan to reasearch and implement:
- Use magnet links to download files

- Use Distributed Hash tables instead of trackers
- Allow for more than one downloads
- Create a graphical interface
- Support pausing and resuming downloads
- Use WebRTC to create direct connection to peers
