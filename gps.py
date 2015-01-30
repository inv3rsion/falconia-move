import urllib2;

def getGPS():
    try:
        data = urllib2.urlopen("http://10.144.7.183/coord.txt").read();
        return [int(i) for i in data.split(",")];
    except:
        print "Could not access coordinates...";

print getGPS();


