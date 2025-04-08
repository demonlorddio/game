import random
import time
print ('''
\t\t\t\t\t\t\t --//WELCOME TO THE MATH QUIZ//--''')
time.sleep(1)
diff=int(input(f'''
select your difficulty:
1-easy
2-medium
3-hard
4-extreme
'''))
time.sleep(2)    
    
game=True
score=0
highscore=0
while game:
    o=['+','-','x','%']
    opp=random.choice(o)
    if diff == 1:
        a=random.randint(0,10)
        b=random.randint(0,10)
    elif diff == 2:
        a=random.randint(10,100)
        b=random.randint(10,100)
    elif diff == 3:
        a=random.randint(50,150)
        b=random.randint(50,150)
    elif diff == 4:
        a=random.randint(100,1000)
        b=random.randint(100,1000)
    print(f'\t\t score:{score}')
    question=f'whats {a}{opp}{b}?\n='
    answer=float(input(question))
    if opp=='+':
        ans=a+b
    elif opp=='-':
        ans=a-b
    elif opp=='x':
        ans=a*b
    elif opp=='%':
        ans=a/b
    if type(ans)==float:
        ans= round(ans,2)
    print('..........')
    time.sleep(3)
    if answer==ans:
        print('correct answer!!')
        score+=1
    else:
        print('wrong answer')
        time.sleep(1)
        print(f'the correct answer was {ans}')
        time.sleep(1)
        print(f'your total score is {score}')
        if score>highscore:
            highscore =score
            score =0
            print('\nA new highscore!!')
            time.sleep(1)
        retry=input(f'''
\t\t\t highscore:{highscore}
\t\t\t score:{score}
would you like to try again?
[y/n]:''')
        if retry=='y':
            continue
        if retry=='n':
            game=False
    time.sleep(2)
