
distcnt=`redis-cli --raw keys area:* | awk '!/selflib.set/{print $0}' | wc -l`
totalbook=0

declare -A assarray
echo "district count:" $distcnt
while read line;do
	echo $line
	bookcnt=0
	for((i=1; i<=distcnt; i++)){
		bookcnt2=0
		for sl in `redis-cli --raw smembers area:$i:selflib.set`;do
			bc=`redis-cli --raw hget selflib:$sl $line.cnt`
			bookcnt=$((bookcnt + bc))
			bookcnt2=$((bookcnt2 + bc))
		done
		echo `redis-cli --raw hget area:$i name` " " $bookcnt2
		totalbook=$((totalbook + bookcnt))
	}
	assarray[${line}]=$bookcnt
	echo ${assarray[$line]}
done < category.txt

echo "total selflib count: " $totalbook
