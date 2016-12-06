Running
----------------------------------------------------------------------------
usage: DicSetup <database size> <Hashtag> <mode> <parm>
       database size: the num of tweets collected from twitter
  	   mode: either 'streaming' or 'msg'
  	   parm: int number of the incoming tweets for mode 'streaming'
  	   		 or string for the mode 'msg'
       Default: 2000 '#Trump' streaming 5
       Running sample: python DicSetup.py 5000 NBA streaming 10
              	   or: python DicSetup.py 5000 NBA msg " rt XXX..."

Files
----------------------------------------------------------------------------
System will generate the dictionary file with the name of hashtag and another file for debug only

After the system collected tweets from internet, the tweet information will store in the file with name "streaming_result.txt" with the risk level. Meanwhile, the log file will be generated for checking the computation of the risk level.

frequency.txt is the file the most common words in Project Gutenberg: These lists are the most frequent words, when performing a simple, straight (obvious) frequency count of all the books found on Project Gutenberg. I took the first 300 words from the Project Gutenberg

Notice
----------------------------------------------------------------------------
If the dictionary file is already on the disk, but you want to change the search_number, maybe from 5000 to 2000, please delete the dictionay file and then rerun the code

For the mode 'msg', the result will not be stored in the file, 'streaming_result.txt' but only store in the file, 'streaming_log.txt'