
distcnt=`redis-cli --raw keys area:* | awk '!/selflib.set/{print $0}' | wc -l`
totalbook=0

echo "district count:" $distcnt
for((i=1; i<=distcnt; i++)){
	bookcnt=0
	redis-cli --raw hget area:$i name;
	for sl in `redis-cli --raw smembers area:$i:selflib.set`;do
		bookcnt=$((bookcnt + `redis-cli --raw hget selflib:$sl book.cnt`))
	done
	echo $bookcnt
	totalbook=$((totalbook + bookcnt))
}

echo "total selflib count: " $totalbook
