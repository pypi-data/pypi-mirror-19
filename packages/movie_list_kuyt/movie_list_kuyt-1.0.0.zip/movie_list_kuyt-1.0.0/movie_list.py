movies =['a','b',['c','d',['e','f','g']]]
def check_list(lists,level):
    for i in lists:
        if not isinstance(i, list):
            
            for j in range(level):
                print("_______",end='*')
            print(i)
        else:
            level -= 1
            check_list(i,level)
check_list(movies,5)            
        
