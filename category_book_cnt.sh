
distcnt=`redis-cli --raw keys area:* | awk '!/selflib.set/{print $0}' | wc -l`
totalbook=0

declare -A assarray
echo "district count:" $distcnt
while read line;do
	echo $line
	bookcnt=0
	for((i=1; i<=distcnt; i++)){
#		redis-cli --raw hget area:$i name;
		for sl in `redis-cli --raw smembers area:$i:selflib.set`;do
			bookcnt=$((bookcnt + `redis-cli --raw hget selflib:$sl $line.cnt`))
		done
		totalbook=$((totalbook + bookcnt))
	}
	assarray[${line}]=$bookcnt
	echo ${assarray[$line]}
done < category.txt

echo "total selflib count: " $totalbook
