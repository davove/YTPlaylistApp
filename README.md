# YTPlaylistApp
A little app for organizing playlists into neat txt files, and catching removed songs using Waybackpy:

I noticed that Youtube would sometimes remove songs I liked and had in playlists, and give no indication of the song they removed. Otherwise, a channel might get privated or choose to delete the video themselves. Already, many of these "corrupted" songs are in my playlists, so I decided that rather than going song-by-song to figure things out, I wanted to make a program to help prevent this from happening further, and to reduce the damage already done.

Handling and storing playlists is important not only for my own record-keeping, but also because it would allow me to find missing songs without having to load WaybackMachine with requests. Ideally, waybackpy could be used for handling songs that I don't have a backed-up list to determine, but the program itself should contain the necessary tools to create and store playlist files for viewing by me, and as a first step to finding a corrupt song.

