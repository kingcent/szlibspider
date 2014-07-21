
distcnt=`redis-cli --raw keys area:* | awk '!/selflib.set/{print $0}' | wc -l`
totalsc=0

echo "district count:" $distcnt
for((i=1; i<=distcnt; i++)){
	redis-cli --raw hget area:$i name;
	sc=`redis-cli --raw hget area:$i selflib.cnt`;
	echo $sc;
	totalsc=$((totalsc + sc))
}

echo "total selflib count: " $totalsc
