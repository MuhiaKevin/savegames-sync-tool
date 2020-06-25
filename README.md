# savegames-sync-tool

A tool to upload my save games to disk and Google Drive.

## How to use

1. Set paths savegame to locations in the dirs.txt file 
2. Change the global variable name 'DEST' to location of where you want backup the savegames
3. Run below command to install required packages:
```sh
$ python -m pip install -r requirements.txt 
```

4. Run the Command bellow to execute the program:
```sh
$ python3 main.py 
```

## TODO 
* Add notifications when completed backing up savegames


## Future improvements
* [x] Read dir.txt file and check if the directory exists
* [x] If folder exists check if it is saved in the database
* [x] If folder exists and is in the database, check if the sha1 value of the folder is the same as that in the database
* [ ] If it has changed add folder to queue and schedule it for upload to cloud
* [ ] If it has not changed then leave it as it is
* [ ] If folder does not exist then throw error



## Resources

https://pypi.org/project/checksumdir/1.0.5/
https://stackoverflow.com/questions/24937495/how-can-i-calculate-a-hash-for-a-filesystem-directory-using-python
https://www.digitalocean.com/community/tutorials/how-to-use-the-sqlite3-module-in-python-3
https://realpython.com/read-write-files-python/
https://www.codecademy.com/articles/what-is-sqlite
https://codelabs.developers.google.com/codelabs/gsuite-apis-intro/#4
https://levelup.gitconnected.com/google-drive-api-with-python-part-ii-connect-to-google-drive-and-search-for-file-7138422e0563
