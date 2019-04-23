echo "--------------------" >> ./LOG_CMD.txt
date '+%Y-%m-%d %H:%M:%S' >> ./LOG_CMD.txt
echo "Run command: "$@ >> ./LOG_CMD.txt
echo "--------------------" >> ./LOG_CMD.txt

# Finally, run the scripts' arguments as a command
$@