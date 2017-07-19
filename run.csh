#!/bin/csh

mkdir data
cd data
rm -rf *

set YEAR=`date -u -d '-1 hour' +%Y`
set JDAY=`date -u -d '-1 hour' +%j`
set HOUR=`date -u -d '-1 hour' +%H`
echo $YEAR
echo $JDAY
echo $HOUR

set FILES=`/usr/local/bin/aws s3 ls s3://noaa-goes16/ABI-L2-MCMIPF/$YEAR/$JDAY/$HOUR/ --no-sign-request --endpoint-url https://128.135.112.106:9000 --no-verify-ssl | tr -s " " | cut -d " " -f 4 | grep OR_ABI-L2-MCMIPF-`
foreach FILE ($FILES)
echo $FILE
/usr/local/bin/aws s3 cp s3://noaa-goes16/ABI-L2-MCMIPF/$YEAR/$JDAY/$HOUR/$FILE . --no-sign-request --endpoint-url https://osdc.rcc.uchicago.edu --no-verify-ssl
set DATESTRING=`echo $FILE | cut -d _ -f 4`
set YEARF=`echo $DATESTRING | cut -c2-5`
set JDAYF=`echo $DATESTRING | cut -c6-8`
set HOURF=`echo $DATESTRING | cut -c9-10`
set MINF=`echo $DATESTRING | cut -c11-12`
set MONTHF=`date -d "$JDAYF days $YEARF-01-01 - 1 days" +"%m"`
set DAYF=`date -d "$JDAYF days $YEARF-01-01 - 1 days" +"%d"`
echo $DATESTRING
echo $YEARF
echo $JDAYF
echo $HOURF
echo $MINF
echo $DAYF
echo $MONTHF
../plot.py $FILE g16-$YEARF-$MONTHF-$DAYF-$HOURF-$MINF.png
#scp g16-$YEARF-$MONTHF-$DAYF-$HOURF-$MINF.png somewhereelse
end
