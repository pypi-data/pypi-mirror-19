number=int(input("Please Enter any Number: "))
n=0
while (number>0):
	Reminder=number%10
	n=(n*10)+Reminder
	number=number//10
print ('Reverse of enter Number is=%d' %n)






