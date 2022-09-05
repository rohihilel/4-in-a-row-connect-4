#roee hilel, 328487657



def save(grid):
    f = open('arr.txt', 'r+')
    f.truncate(0)
    for arr in grid:
        for x in arr:
            print(x,file=f,end='')

        print( "",file = f)
    f.close()

def load():
    grid = []
    a = []
    for line in open('arr.txt'):
        a = []
        for i in line.strip():
            a.append(i)
        grid.append(a)



    return grid





