# Description
Script for finding exact copies of files.

This script was created mainly for finding copies of photos in my collection (e.g., sub-collections that were made for printing or sharing, old backups, photos that were organized at some point of time and weren't properly cleaned up), but it works with any kind of files - photos, videos, documents, software installers etc.

# Usage
* Make sure that Python is installed (I used Python 2.7.13).
* Put the script in any directory.
* Open Command Prompt.
* Navigate to the directory which you want to check for duplicates.
* Run the script.
* Make some tea.

# Sample output
<pre>
c:\GitHub\find-duplicates>cd \Pictures

c:\Pictures>\GitHub\find-duplicates\find_duplicates.py
Building list of files... Done, found 40776 files in 536 directories, 154.59 GB
Filtering unique files (by size)... Done, 6306 files left, 22.81 GB
Hashing files... Done
Filtering unique files (by hash)... Done, 4916 files left, 18.46 GB
--------------------------------------------------------------------------------
.\~archive\2006-03-11
    100_2184.jpg:
        .\~misc\photo (old)\100_2184.jpg
        .\~misc\photo (old)\``labas\100_2184.jpg
--------------------------------------------------------------------------------
...
...
...
--------------------------------------------------------------------------------
Zero-sized files:
    .\~sale\HM321HI - Samsung 320GB.txt:
    .\~sale\HTS541616J9SA00 - Hitachi 160GB.txt:
    .\~sale\WD2500BEVS-00UST0 - WD 250GB.txt:
    .\~sale\WD3200BEVT-22ZCT0 - WD 320GB.txt:
--------------------------------------------------------------------------------
Finished in 20.84 seconds
</pre>

# How it works?
* Creates a list of all files in current working directory.
* Filters files by their size - files can't be the same if they have different sizes.
* Creates SHA1 hash for remaining files.
* Compares file hashes - if hashes are equal, script assumes that the files are exact copies.
* Prints list of all duplicates (if any).
* Prints list of all zero-sized files (if any).

# TODO
**High priority**

Add some command line arguments:
* search files - search duplicates of specified files
* list extensions - list file extensions that are present in root directory
* include extensions - search only files with specified extensions
* exclude extensions - skip files with specified extensions

**Low priority**

*Replace hashing files and comparing hashes with comparing actual files?*

Current solution is straightforward and it works perfectly well for me. Hashing (SHA1) is pretty fast. Most of the time is spent on reading files which is not a huge issue when using SSD.

Comparing actual files may be faster, when there are files with the same size, but with different contents. Though, it's slightly harder to implement. Comparing 2 files is easy, comparing and grouping arbitrary number of files while reading them only once takes more effort.

# Donations
Did you find this script useful?<br/>
Did it help you to clean up your photo collection?<br/>
Did it help you in any other way?<br/>
Great!

Do you want to use it for free, without restrictions, at home, in your car or anywhere else?<br/>
Great! Feel free to do it :)

Do you want to make a small donation?<br/>
Oh well, think again.

http://paypal.me/andrejssitals/5

bitcoin:1AgWFzUqcgXng7GKDecNS4f93G1Hi3hX2J
