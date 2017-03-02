#coding=utf-8
i = 1
js = [i]
while i < 10:
    for j in js:
        print "%dX%d=%d" %(i,j,i*j),
    print "\t"
    i += 1
    js.append(i)
