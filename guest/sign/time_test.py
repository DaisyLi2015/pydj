
# current time
import time

now_time = time.time()
print('current timestarp :'+str(now_time))


# convert date style
otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(now_time))
print('date format: ' +str(otherStyleTime))