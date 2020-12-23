rm results.txt
rm -rf webreport
rm jmeter.log

/Users/liqi17thu/Desktop/apache-jmeter-5.4/bin/jmeter -n -t $1 -l ./results.txt -e -o ./webreport