import osuApiAccessor as api


async def calculatePP(user, play, newpp):
    currentTotal = float((await api.getUserByName(user))["pp_raw"])
    usertops = await api.getUserTops(user)
    usertopPP = []
    for pplay in usertops:
        print(pplay["pp"])
        usertopPP.append(float(pplay["pp"]))

    ppBonus = currentTotal - calculateTotal(usertopPP)       #to approximate bonus PP, calculate how much PP comes from scores outside of the top 100. Not entirely accurate but differences are negligible.
    newtopPP = usertopPP
    if(newpp<usertopPP[99]):
        newtopPP[play-1] = usertopPP[99]
    else:
        newtopPP[play-1] = newpp
    newtopPP.sort(reverse=True)   
    newTotal = ppBonus + calculateTotal(newtopPP)
    print("done")
    return [currentTotal, newTotal]



def calculateTotal(usertops):
    i = 0
    totalpp = 0.0
    for play in usertops:
        print(totalpp)
        totalpp+=play*0.95**i                               #top play pp calculation formula is pp*0.95^n, where n is the number of plays above the given play in the users' tops
    return totalpp