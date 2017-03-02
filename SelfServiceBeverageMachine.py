# coding = utf-8


money = 0
def coin():
    loopfunc = True
    global money
    while loopfunc:
        x = raw_input("Please Input coin,press 'q' to exit ")
        if x == 'q':
            if money == 0:
                print "Your coin is 0 and cann`t afford anything! "
            else:
                print "You have Input %s coin." %(x)
                loopfunc = False
        else:
            money += int(x)
            print "The coin is %d yuan. All your coins is %d" %(int(x),money)
    return money
money = coin()
drinklist = {
    'Coca Cola' : 2.5,
    'milky tea' : 1.5,
    'Juce':3,
    'JDB':4
    }
i = 0
print 'Please choose the drink you want to buy'
for x in drinklist:
    i += 1
    print "No. %d drink is %s .The price is %s" % (i,x,drinklist[x])

loop = True
while loop:
    drinkNo = raw_input("Please Input The Drink Num. 'q' to exist")
    if drinkNo == 'q':
        loop = False
    else:
        drinkNo = int(drinkNo)
        if drinkNo >=1 and drinkNo <= 4:
            i = 0
            for x in drinklist:
                i += 1
                if i == drinkNo:
                    if money >= drinklist[x]:
                        money = money - drinklist[x]
                        print "The drink you choos is %s .The Price is %s .Your balance is %s" %(x,drinklist[x],money) 
                    else:
                        print 'Your balance is not enough to buy any drink'
                        money = coin()
        else:
            print "The Drink is not exist!"
        
            print "The Drink No. is not exist"
if money > 0:
    print "Your balance is %s,Welcome again!" % (money)
else:
    print "88"
