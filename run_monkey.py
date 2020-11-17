#-*- coding: UTF-8 -*-  
import os
from subprocess import Popen,PIPE

#get model,version,and brand 
def get_system_info():
	model_output = os.popen("adb shell cat /system/build.prop |grep 'ro.product.model'|head -1")
	model = model_output.read().strip('\n').split('=')[1]
	version_output = os.popen("adb shell cat /system/build.prop |grep -e 'ro.build.version.release'")
	version = version_output.read().strip('\n').split('=')[1]
	brand_output = os.popen("adb shell cat /system/build.prop |grep -e 'ro.product.brand'")
	brand = brand_output.read().strip('\n').split('=')[1]
	return [model,version,brand]

#write system info to report file
report_name = "report.log"
f=open(report_name,'a')
f.write("===========================================稳定性测试报告========================================\n\n\n")
f.write("===========================================测试设备设备信息======================================\n")
f.write("手机型号: "+get_system_info()[0]+"\n")
f.write("手机OS版本："+get_system_info()[1]+"\n")
f.write("手机厂商: "+get_system_info()[2]+"\n")
f.write("===========================================各种异常发生情况统计===================================\n")

#清空logcat信息
Popen("adb logcat -c", shell=True,stdout=PIPE, stderr=PIPE).stdout.readlines()
logcat_file = open("logcat.log", 'w')
#保存logcat信息
process_logcat = Popen('adb logcat -v time', shell=True, stdout=logcat_file)

#运行monkey脚本,并把log重定向到monkey.log文件
monkey_execute_cmd = 'adb shell monkey -p com.example.activitytest --throttle 100 --ignore-crashes --ignore-timeouts --ignore-security-exceptions --ignore-native-crashes --monitor-native-crashes -v -v -v 5000 > monkey.log'
os.system(monkey_execute_cmd)
#过滤出CRASH的log并取后面的5行记录并重定向到exceptions.log
#后续可能还有ARN之类的错误，到时候在添加对应的逻辑
os.system("grep -A 15 -h -r CRASH monkey.log > exceptions_monkey.log")
crash_count = os.popen("grep -c '// CRASH' exceptions_monkey.log").read()
f.write("发生CRASH次数："+crash_count+"\n")


f.write("===========================================monkey log辅助信息===================================\n")
f.close()
#将过滤出来的monkey.log追加到测试报告中
os.system("cat exceptions_monkey.log  >> report.log")

process_logcat.terminate()

os.system("echo '\n\n=======================================Logcat辅助信息=======================================\n' >> report.log")
# f.write("\n\n\=======================================Logcat辅助信息=======================================\n")
# f.close()
#过滤logcat中出现错误处的信息到测试报告中
os.system("grep -A 20 -h -r 'java.lang.NullPointerException' logcat.log >> report.log")
os.system("grep -A 20 -h -r 'java.lang.IllegalStateException' logcat.log >> report.log")
os.system("grep -A 20 -h -r 'java.lang.IllegalArgumentException' logcat.log >> report.log")
os.system("grep -A 20 -h -r 'java.lang.ArrayIndexOutOfBoundsException' logcat.log >> report.log")
os.system("grep -A 20 -h -r 'java.lang.RuntimeException' logcat.log >> report.log")
os.system("grep -A 20 -h -r 'java.lang.SecurityException' logcat.log >> report.log")
