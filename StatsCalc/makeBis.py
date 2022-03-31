import pandas as pd
import numpy as np
from itertools import combinations, product
from os.path import exists

def as_list(x):
    if type(x) is list:
        return x
    else:
        return [x]

def calcAllPossibilitiesForGear(usedBy = ["Mail","All","Healers"]):
    """
    Calcs all possibilties for gear for a given class
    Weapons are not Included
    returns itemlist and calculated stats for gear
    """
    try:
        df = pd.read_csv("RoA_Items.csv")
    except Exception as e:
        raise Exception("no RoA_Items.csv brug", e)

    mailtank27 = df.loc[(df["Item LVL"] == 27) & (df["Used By"].isin(usedBy))].copy().fillna(0)

    heads = mailtank27.loc[(mailtank27["Item Type"] == "Head")].copy()
    shoulders = mailtank27.loc[(mailtank27["Item Type"] == "Shoulders")].copy()
    chests = mailtank27.loc[(mailtank27["Item Type"] == "Chest")].copy()
    hands = mailtank27.loc[(mailtank27["Item Type"] == "Hands")].copy()
    belts = mailtank27.loc[(mailtank27["Item Type"] == "Belt")].copy()
    legs = mailtank27.loc[(mailtank27["Item Type"] == "Legs")].copy()

    #cloak, bracers or boots 
    secondarys = mailtank27.loc[(mailtank27["Item Type"] == "Secondary - Boots") | (mailtank27["Item Type"] == "Secondary - Bracers") | (mailtank27["Item Type"] == "Secondary - Cloak")].copy()
    #neck, ring or trinket
    trinkets = mailtank27.loc[(mailtank27["Item Type"] == "Jewelry - Neck") | (mailtank27["Item Type"] == "Jewelry - Ring") | (mailtank27["Item Type"] == "Jewelry - Trinket")].copy()

    headsIx = list(heads.index)
    shouldersIx = list(shoulders.index)
    chestsIx = list(chests.index)
    handsIx = list(hands.index)
    beltsIx = list(belts.index)
    legsIx = list(legs.index)
    secondarysIx = list(secondarys.index)
    trinketsIx = list(trinkets.index)

    allPossibilities = list(x for x in product(headsIx, shouldersIx, chestsIx, handsIx, beltsIx, legsIx, secondarysIx, trinketsIx))

    #Gear without Weapon

    if exists("calc_stats.csv"):
        gearsetDF = pd.read_csv("calc_stats.csv") 
    else:
        a = []
        for x in allPossibilities:
            gearset = mailtank27.loc[list(x)].sum(numeric_only = True)
            gearset["Items"] = list(x)
            del gearset["Item LVL"]
            a.append(gearset)
            print(x)

        gearsetDF = pd.DataFrame(data=a)
        gearsetDF.to_csv("calc_stats.csv")
    
    return mailtank27, gearsetDF

#gearset = mailtank27.loc[list(allPossibilities[0])].sum(numeric_only = True)




def calcAllPossibilitiesForWeapons(mailtank27):
    """
    Calcs all Weapon Possibilties for given Itemlist
    returns weapons
    """
    #Weapons
    mhand = mailtank27.loc[(mailtank27["Item Type"] == "Main Hand")].copy()
    ohand = mailtank27.loc[(mailtank27["Item Type"] == "Off Hand") | (mailtank27["Item Type"] == "Shield")].copy()

    mhandIx = list(mhand.index)
    ohandIx = list(ohand.index)

    mhAndOh = list(x for x in product(mhandIx, ohandIx))

    pair = []
    for x in mhAndOh:
        gearset = mailtank27.loc[list(x)].sum(numeric_only = True)
        gearset["Items"] = list(x)
        del gearset["Item LVL"]
        pair.append(gearset)
    #hehe = gearset = mailtank27.loc[list(allPossibilities[0])].sum(numeric_only = True)
    pairDF = pd.DataFrame(data=pair)

    twoHand = mailtank27.loc[(mailtank27["Item Type"] == "Two Hand")].copy()
    del twoHand["Name"]
    del twoHand["Drops From"]
    del twoHand["Item Type"]
    del twoHand["Used By"]
    del twoHand["Item LVL"]
    twoHand["Items"] = twoHand.index

    pairIx = list(pairDF.index)
    twoHandIx = list(twoHand.index)
    #mh + oh(shield/oh) or 2hand
    return pd.concat([pairDF, twoHand])

    #gearsetIx = list(gearsetDF.index)
    #weaponsIx = list(weaponsDF.index)

def mergeGearAndWeapons(gearsetDF, weaponsDF, statPrio=["SP","Versatility", "Mastery"]):
    """
    merges the gear and weapons
    returns the indexes for itemlist
    """
    gearsetIx = list(gearsetDF.index)
    weaponsIx = list(weaponsDF.index)    

    print("Weapon Possibilities calculated")
    #merged 
    equipmentPossibilities = list(x for x in product(gearsetIx, weaponsIx))

    if exists("all_gears_new.csv"):
        equipmentDF = pd.read_csv("all_gears_new.csv")

    else:
        equip = []
        for x in equipmentPossibilities:
            gearset = gearsetDF.loc[x[0]].iloc[1:-1].copy()
            weap = weaponsDF.loc[x[1]].iloc[:-1].copy()
            gearsetItems = gearsetDF.loc[x[0]].iloc[-1:].copy()
            weapItems = weaponsDF.loc[x[1]].iloc[-1:].copy()

            gear = gearset + weap
            gear["Items"] = list(map(int, gearsetItems.values[0][1:-1].split(","))) + as_list(weapItems.values[0])
            print(x)
            equip.append(gear)

        equipmentDF =  pd.DataFrame(data=equip)
        equipmentDF.to_csv("all_gears_new.csv")


    index = equipmentDF.sort_values(by=statPrio, ascending=False).iloc[0]["Items"]
    if isinstance(index, str):
        index = list(map(int,index[1:-1].split(",")))
    return index


if __name__ == "__main__":
    usedBy = ["Mail","All","Healers"]
    statPrio=["SP","Versatility", "Mastery"]


    mailtank27, gearsetDF = calcAllPossibilitiesForGear(usedBy)
    print("RoA Items loaded")
    print("All Possibilities for Gear calculated")
    weaponsDF = calcAllPossibilitiesForWeapons(mailtank27)
    print("All Possibilities for Weapons calculated")

    index = mergeGearAndWeapons(gearsetDF, weaponsDF, statPrio)
    #TODO: make logic for given specific numbers for stats like Mastery >= 200


    #print shit to farm
    print(mailtank27.loc[index,["Name","Drops From"]])

    #print sumed up stats for gear
    print(mailtank27.loc[index].iloc[:,5:].sum())



"""
a = equipmentDF.sort_values(by=["Health","Armor", "SP", "DR"], ascending=False).iloc[0]["Items"]
for i in a:
    print(mailtank27.loc[i]["Name"])
"""



"""
mydf.loc[(mydf["Item Type"] == "Chest" ),               "Health"] =             mydf["Health"] * 2
for a in product(headsIx, shouldersIx, chestsIx, handsIx, beltsIx, legsIx, secondarysIx, trinketsIx):
    print(a)
    break


#print(list(x for x in product(headsIx, shouldersIx, chestsIx, handsIx, beltsIx, legsIx, secondarysIx, trinketsIx)))
"""
"""
a = [[111,112,113], [222,223,225], [(33,34),44]]
comb = product(*a)

for a in comb:
    print(a)
"""