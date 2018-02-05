#!/bin/bash
FILENAME=conf_list.config
LOCAL_PATH=/tmp/base_rules
NEW_PATH=/tmp/new_conf
TALL=",setvar:tx.hit_block_count=+1,setvar:tx.hit_all_ruleid=%{tx.hit_all_ruleid}+%{rule.id}\""

function READ_FILENAME_LINE(){

if [ ! -d "$NEW_PATH" ]; then
        echo $NEW_PATH;
        mkdir "$NEW_PATH";
 else
        echo "$NEW_PATH already have"
	rm $NEW_PATH/*
fi

while read LINE
do
   echo $LINE
	
   if [ ! -f "$NEW_PATH/$LINE" ]; then
   	cp $LOCAL_PATH/$LINE $NEW_PATH/$LINE
   else 
   	echo "$NEW_PATH/$LINE already have"
   fi

done < $FILENAME
}


#for conf in ${conf_file_list}
#do
 #  echo $conf
#done
function DEAL_CHAIN()
{
   # chain 行后加\
   sed -i -e '/\<chain\>/s/$/\\/' $1.tmp
   #sed -i -e ':a;N;$!ba;s/\n//g'  $1.tmp
   # 将 chain \ 后与前一行合并为一行
   sed -i -e :a -e '/\\$/N; s/\\\n//; ta' $1.tmp
   
}

function DEAL_LINE(){
#  echo "$1"
# 这里read需要 + r 参数，否则字符查中反斜杠会被当作转义字符来看
all_idx=0
need_tail_idx=0
no_tail_idx=0
chain_idx=0

while read -r LINE
do 
   let all_idx=$all_idx+1
   phase1_result=$(echo $LINE | grep  "phase:1")
   phase2_result=$(echo $LINE | grep  "phase:2")
   block_result=$(echo $LINE | grep   "block")
   chain_result=$(echo $LINE | grep   "chain")
if [[ ("$chain_result" != "") ]]

 then
   #echo "chain"
   let chain_idx=$chain_idx+1

fi

  # echo $result
if [[ (("$phase1_result" != "")||("$phase2_result" != ""))&&("$block_result" != "") ]]
#if [[ (($LINE =~ $STRA1)||($LINE =~ $STRA2))&&($LINE =~ $STRB) ]]
 then
 #    echo "包含"
# 去除尾部字符 再加上新的尾部
     let need_tail_idx=$need_tail_idx+1
     line_result=${LINE%?}${TALL}
     echo "$line_result" >> $1.new

#     sed  's/.$//' $LINE |sed  's/$/&,setvar:tx.test_block=+1,setvar:tx.all_id=%{tx.all_id}+%{rule.id},setvar:tx.test_id=%{rule.id}"/g'
 else
     #echo "不包含"
     let no_tail_idx=$no_tail_idx+1
     echo "$LINE" >>$1.new
 fi
 
done <$1.tmp
sed -i "s/SecRule/\nSecRule/g"  $1.new
echo  "file:$1, all_idx is:$all_idx, need_tail_idx is:$need_tail_idx, no_tail_idx is:$no_tail_idx, chain_idx is:$chain_idx"
rm  $1.tmp
mv $1.new $1

}

function CREATE_NEW_CONF(){

for file_name in ${NEW_PATH}/*
do
   echo $file_name

#1去除首部空格和tab.2去除尾部空格和tab 3去除注释 4去除结尾\（反斜杠）5 去除空行 6 规则与规则之间加入换行  > 中间文件 7 处理SecMarker
sed -e "s/^[ \t]*//g" $file_name|sed -e "s/[ \t]*$//g" |sed -e "s/^#.*//g" |sed -e  "s/\\\\$//g"|sed ':a;N;$!ba;s/\n//g'|sed -e "s/SecRule/\nSecRule/g"|sed -e "s/SecMarker/\nSecMarker/g" > ${file_name}.tmp

DEAL_CHAIN ${file_name}
DEAL_LINE ${file_name}

#awk -F: '{ phase_result = match($0,"phase:2");block_result = match($0,"block");if(phase_result > 0&&block_result > 0) { sub_str=gensub(/"$/,"${TALL}\"",1,$0);print sub_str} else {print $0} ;}' ${FILE}.tmp >${FILE}.new
done

}


READ_FILENAME_LINE;

CREATE_NEW_CONF;
