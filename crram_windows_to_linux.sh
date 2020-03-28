#!/bin/sh
FILE="C:\Projects\MRI\analysis\analysis.html"
value=`cat $FILE`
echo "${value//'src\'/'src/'}" > $FILE      
