# savegames-sync-tool

A tool to upload my save games to Google Drive


### Future improvements
* [x] Read dir.txt file and check if the directory exists
* [x] If folder exists check if it is saved in the database
* [x] If folder exists and is in the database, check if the sha1 value of the folder is the same as that in the database
* [ ] If it has changed add folder to queue and schedule it for upload to cloud
* [ ] If it has not changed then leave it as it is
* [ ] If folder does not exist then throw error

### Future improvements
These are some of the additional features i plan to reasearch and implement:
- Use magnet links to download files

- Use Distributed Hash tables instead of trackers
- Allow for more than one downloads
- Create a graphical interface
- Support pausing and resuming downloads
- Use WebRTC to create direct connection to peers
