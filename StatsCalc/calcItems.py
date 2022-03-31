import pandas as pd
import numpy as np

#constants
sheet_url = "https://docs.google.com/spreadsheets/d/1yqYdsnk4TpKKvdD-2BxfjVPEzhAez15Xc0VGwV3vuow/edit#gid=0"
url = sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")
stats = ["Health", "HP Regen", "Armor", "DR", "Block", "Resource", "R Regen", "SP", "Crit Chance", "Crit Force", "Mastery", "Versatility", "AP", "AS", "MS"]
mainstats = [   ("Chest",               "Health"),
                ("Secondary - Cloak",   "HP Regen"),
                ("Shoulders",           "Armor"),
                ("Hands",               "DR"),
                ("Shield",              "Block"),
                ("Head",                "Resource"),
                ("Secondary - Bracers", "R Regen"),
                ("Jewelry - Trinket",   "SP"),
                ("Jewelry - Neck",      "Crit Chance"),
                ("Belt",                "Crit Force"),
                ("Legs",                "Mastery"),
                ("Jewelry - Ring",      "Versatility"),
                ("Secondary - Boots",    "MS")
]
statscaling = [ (8   , "Health"),
                (0.1 , "HP Regen"),
                (0.2 , "Armor"),
                (0.2 , "DR"),
                (0.17, "Block" ),
                (0.8 , "Resource" ),
                (0.02, "R Regen"),
                (1   , "SP" ),
                (0.2 , "Crit Chance"),
                (0.3 , "Crit Force"),
                (0.8 , "Mastery" ),
                (0.25, "Versatility" ),
                (0.5 , "AP" ),
                (0.4 , "AS" ),
                (0.35, "MS")
]
specificScaling = [     ("Two Hand", "AP", "SP"),
                        ("Main Hand", "AP", "SP"),
                        ("Off Hand", "AS", "SP")
]

#read mezis droplist
df = pd.read_csv(url)
#remove all current HC Items
df = df[df["Item LVL"] != 23]

hcitems = df[df["Item LVL"] != 27].copy()
hcitems.loc[:,"Item LVL"] = 23
hcitems.loc[:,"Drops From"] = hcitems["Drops From"].apply(lambda x: "{}HC -{}".format(x.split("-")[0], x.split("-")[-1]))

upitems = hcitems.copy()
upitems.loc[:,"Item LVL"] = 27
upitems.loc[:,"Drops From"] = hcitems["Drops From"].apply(lambda x: "{}Upgraded -{}".format(x.split("-")[0], x.split("-")[-1]))

df = pd.concat([df, hcitems, upitems])

df = df.fillna(0)
for stat in stats:
        df.loc[(df[stat] != 0.0 ), stat] = 1

data = df.to_dict("list")

mydf = pd.DataFrame.from_dict(data)

#set stat scaling 
for value, stat in statscaling:
        mydf[stat] = mydf["Item LVL"] * value * mydf[stat]

# Update Stats: if main stat -> 2 * value
for piece, stat in mainstats:
       mydf.loc[(mydf["Item Type"] == piece ), stat] = mydf[stat] * 2

#Two Hand Weapons have all stats doubled
for stat in stats:
        mydf.loc[(mydf["Item Type"] == "Two Hand" ), stat] = mydf[stat] * 2

#class specific scaling 
for piece, stat, stat2 in specificScaling:
        mydf.loc[(mydf["Item Type"] == piece) & (~mydf["Used By"].isin(["Healers", "INT DD"]) ), stat] = mydf[stat] * 2
        mydf.loc[(mydf["Item Type"] == piece) & (mydf["Used By"].isin(["Healers", "INT DD"]) ), stat2] = mydf[stat2] * 2

#dirty truncate
for stat in stats:
        mydf[stat] = (mydf[stat] * 10).astype(int).astype(float) / 10 
#make 0.0 appear blank in sheet
for stat in stats:
        mydf[stat] = mydf[stat].replace(0,np.nan)


mydf.to_html("temp2.html")
mydf.to_csv("RoA_Items.csv", index=False)
#print(mydf)


"""
mailtank27 = df.loc[(df["Item LVL"] == 27) & (df["Used By"].isin(["Mail","All","Tanks"]))]
mailtank27.to_html("temp.html")

testdata = {"Name":["Medallion of Steadfast Might","insane good item", "Earthfury Vestments", "bigarmor", "Staff of Hale Magefire", "Venomstrike" ],
        "Drops From":["MC - Magmadar", "ukraine at tordes house", "MC - Garr", "hehexd", "MC - Ragnaros", "WC - Lord Cobrahn"],
        "Item Type" :["Jewelry - Neck", "godtier", "Chest", "Chest", "Two Hand", "Two Hand"],
        "Used By" :["All", "noone", "Mail", "Mail", "Healers", "Hunters"],
        "Item LVL" :[27, 27, 27, 13, 27, 13],
        "Health" :[0, 1, 1, 1,0,0],
        "HP Regen":[0, 1, 0, 0,0,0],
        "Armor" :[0, 1, 0, 0,0,0],
        "DR" :[0, 1, 0, 1,0,0],
        "Block" :[0, 1, 0, 0,0,0],
        "Resource" :[0, 1, 0, 0,1,1],
        "R Regen" :[0, 1, 0, 1,0,0],
        "SP" :[1, 1, 0, 0,1,1],
        "Crit Chance" :[1, 1, 0, 0,0,0],
        "Crit Force":[0, 1, 1, 0,0,1],
        "Mastery" :[0, 1, 1, 0,0,0],
        "Versatility" :[1, 1, 1, 1,0,0],
        "AP" :[1, 1, 0, 0,1,1],
        "AS" :[0, 1, 0, 0,1,0],
        "MS":[0, 1, 0, 0,0,0] }

mydf.loc[(mydf["Item Type"] == "Chest" ),               "Health"] =             mydf["Health"] * 2
mydf.loc[(mydf["Item Type"] == "Secondary - Cloak" ),   "HP Regen"] =           mydf["HP Regen"] * 2
mydf.loc[(mydf["Item Type"] == "Shoulders" ),           "Armor"] =              mydf["Armor"] * 2
mydf.loc[(mydf["Item Type"] == "Hands" ),               "DR"] =                 mydf["DR"] * 2
mydf.loc[(mydf["Item Type"] == "Shield" ),              "Block"] =              mydf["Block"] * 2
mydf.loc[(mydf["Item Type"] == "Head"),                 "Resource"] =           mydf["Resource"] * 2
mydf.loc[(mydf["Item Type"] == "Secondary - Bracers" ), "R Regen"] =            mydf["R Regen"] * 2
mydf.loc[(mydf["Item Type"] == "Jewelry - Trinket"),    "SP"] =                 mydf["SP"] * 2
mydf.loc[(mydf["Item Type"] == "Jewelry - Neck" ),      "Crit Chance"] =        mydf["Crit Chance"] * 2
mydf.loc[(mydf["Item Type"] == "Belt" ),                "Crit Force"] =         mydf["Crit Force"] * 2
mydf.loc[(mydf["Item Type"] == "Legs" ),                "Mastery"] =            mydf["Mastery"] * 2
mydf.loc[(mydf["Item Type"] == "Jewelry - Ring" ),      "Versatility"] =        mydf["Versatility"] * 2
mydf.loc[(mydf["Item Type"] == "Secondary - Boots"),    "MS"] =                 mydf["MS"] * 2
"""

"""
mydf.loc[(mydf["Item Type"] == "Two Hand" ),            "Health"] =             mydf["Health"] * 2
mydf.loc[(mydf["Item Type"] == "Two Hand" ),            "HP Regen"] =           mydf["HP Regen"] * 2
mydf.loc[(mydf["Item Type"] == "Two Hand" ),            "Armor"] =              mydf["Armor"] * 2
mydf.loc[(mydf["Item Type"] == "Two Hand" ),            "DR"] =                 mydf["DR"] * 2
mydf.loc[(mydf["Item Type"] == "Two Hand" ),            "Block"] =              mydf["Block"] * 2
mydf.loc[(mydf["Item Type"] == "Two Hand" ),            "Resource"] =           mydf["Resource"] * 2
mydf.loc[(mydf["Item Type"] == "Two Hand" ),            "R Regen"] =            mydf["R Regen"] * 2
mydf.loc[(mydf["Item Type"] == "Two Hand" ),            "SP"] =                 mydf["SP"] * 2
mydf.loc[(mydf["Item Type"] == "Two Hand" ),            "Crit Chance"] =        mydf["Crit Chance"] * 2
mydf.loc[(mydf["Item Type"] == "Two Hand" ),            "Crit Force"] =         mydf["Crit Force"] * 2
mydf.loc[(mydf["Item Type"] == "Two Hand" ),            "Mastery"] =            mydf["Mastery"] * 2
mydf.loc[(mydf["Item Type"] == "Two Hand" ),            "Versatility"] =        mydf["Versatility"] * 2
mydf.loc[(mydf["Item Type"] == "Two Hand"),             "AP"] =                 mydf["AP"] * 2
mydf.loc[(mydf["Item Type"] == "Two Hand"),             "AS"] =                 mydf["AS"] * 2
mydf.loc[(mydf["Item Type"] == "Two Hand" ),            "MS"] =                 mydf["MS"] * 2
"""

"""
mydf["Health"] = mydf["Item LVL"]               * 8            * mydf["Health"] #* (2 if any(mydf["Item Type"] == "Chest") else 1)
mydf["HP Regen"] = mydf["Item LVL"]             * 0.1          * mydf["HP Regen"]#* (2 if any(mydf["Item Type"] == "Cloak") else 1)
mydf["Armor"] = mydf["Item LVL"]                * 0.2          * mydf["Armor"] #* (2 if any(mydf["Item Type"] == "Shoulders") else 1)
mydf["DR"] = mydf["Item LVL"]                   * 0.2          * mydf["DR"] #* (2 if any(mydf["Item Type"] == "Hands") else 1)
mydf["Block" ] = mydf["Item LVL"]               * 0.17         * mydf["Block" ]#* (2 if any(mydf["Item Type"] == "Shield") else 1)
mydf["Resource" ] = mydf["Item LVL"]            * 0.8          * mydf["Resource" ]#* (2 if any(mydf["Item Type"] == "Head") else 1)
mydf["R Regen"] = mydf["Item LVL"]              * 0.02         * mydf["R Regen"]#* (2 if any(mydf["Item Type"] == "Bracers") else 1)
mydf["SP" ] = mydf["Item LVL"]                  * 1            * mydf["SP" ]#* (2 if any(mydf["Item Type"] == "Trinket") else 1)
mydf["Crit Chance"] = mydf["Item LVL"]          * 0.2          * mydf["Crit Chance"]#* (2 if any(mydf["Item Type"] == "Jewelry - Neck") else 1)
mydf["Crit Force"] = mydf["Item LVL"]           * 0.3          * mydf["Crit Force"]#* (2 if any(mydf["Item Type"] == "Belt") else 1)
mydf["Mastery" ] = mydf["Item LVL"]             * 0.8          * mydf["Mastery" ]#* (2 if any(mydf["Item Type"] == "Legs") else 1)
mydf["Versatility" ] = mydf["Item LVL"]         * 0.25         * mydf["Versatility" ]#* (2 if any(mydf["Item Type"] == "Ring") else 1)
mydf["AP" ] = mydf["Item LVL"]                  * 0.5          * mydf["AP" ]#* (2 if any(mydf["Item Type"] == "Main Hand") else 1)
mydf["AS" ] = mydf["Item LVL"]                  * 0.4          * mydf["AS" ]#* (2 if any(mydf["Item Type"] == "Off Hand") else 1)
mydf["MS"] = mydf["Item LVL"]                   * 0.35         * mydf["MS"] #* (2 if any(mydf["Item Type"] == "Boots") else 1)
"""

"""     
mydf["Health"] =        (mydf["Health"] * 10).astype(int).astype(float) / 10
mydf["HP Regen"] =      (mydf["HP Regen"] * 10).astype(int).astype(float) / 10
mydf["Armor"] =         (mydf["Armor"] * 10).astype(int).astype(float) / 10
mydf["DR"] =            (mydf["DR"] * 10).astype(int).astype(float) / 10
mydf["Block" ] =        (mydf["Block"] * 10).astype(int).astype(float) / 10
mydf["Resource" ] =     (mydf["Resource"] * 10).astype(int).astype(float) / 10
mydf["R Regen"] =       (mydf["R Regen"] * 10).astype(int).astype(float) / 10
mydf["SP" ] =           (mydf["SP"] * 10).astype(int).astype(float) / 10
mydf["Crit Chance"] =   (mydf["Crit Chance"] * 10).astype(int).astype(float) / 10
mydf["Crit Force"] =    (mydf["Crit Force"] * 10).astype(int).astype(float) / 10
mydf["Mastery" ] =      (mydf["Mastery" ] * 10).astype(int).astype(float) / 10
mydf["Versatility" ] =  (mydf["Versatility"] * 10).astype(int).astype(float) / 10
mydf["AP" ] =           (mydf["AP"] * 10).astype(int).astype(float) / 10
mydf["AS" ] =           (mydf["AS"] * 10).astype(int).astype(float) / 10
mydf["MS"] =            (mydf["MS"] * 10).astype(int).astype(float) / 10
"""

"""
# todo
mydf.loc[(mydf["Item Type"] == "Two Hand"),             "AP"] =                 mydf["AP"] * 2
mydf.loc[(mydf["Item Type"] == "Main Hand"),            "AP"] =                 mydf["AP"] * 2
mydf.loc[(mydf["Item Type"] == "Off Hand"),             "AS"] =                 mydf["AS"] * 2
# Healers and Int DD weapons have SP as Main Stat
mydf.loc[(mydf["Used By"] == "INT DD"),                 "SP"] =                 mydf["SP"] * 2
mydf.loc[(mydf["Used By"] == "Healers"),                "SP"] =                 mydf["SP"] * 2
"""

"""
#class specific 2Hands
mydf.loc[(mydf["Item Type"] == "Two Hand") & (~mydf["Used By"].isin(["Healers","INT DD"]) ),"AP"] =             mydf["AP"] * 2
mydf.loc[(mydf["Item Type"] == "Two Hand") & (mydf["Used By"].isin(["Healers","INT DD"])), "SP"] =              mydf["SP"] * 2
#mydf.loc[(mydf["Item Type"] == "Two Hand") & (mydf["Used By"] == ),             "SP"] =                 mydf["SP"] * 2

# Main Hand AP
mydf.loc[(mydf["Item Type"] == "Main Hand") & (~mydf["Used By"].isin(["Healers","INT DD"]) ),"AP"] =            mydf["AP"] * 2
mydf.loc[(mydf["Item Type"] == "Main Hand") & (mydf["Used By"].isin(["Healers","INT DD"])), "SP"] =             mydf["SP"] * 2

# Off Hand AP
mydf.loc[(mydf["Item Type"] == "Off Hand") & (~mydf["Used By"].isin(["Healers","INT DD"]) ),"AS"] =             mydf["AS"] * 2
mydf.loc[(mydf["Item Type"] == "Off Hand") & (mydf["Used By"].isin(["Healers","INT DD"])), "SP"] =              mydf["SP"] * 2
"""

"""
"Chest" 
"Cloak" 
"Shoulders" 
"Hands" 
"Shield" 
"Head"
"Bracers" 
"Trinket"
"Jewelry - Neck" 
"Belt" 
"Legs" 
"Ring" 
"Main Hand"
"Off Hand"
"Boots"


"Health"
"HP Regen"
"Armor"
"DR"
"Block"
"Resource"
"R Regen"
"SP"
"Crit Chance"
"Crit Force"
"Mastery"
"Versatility"
"AP"
"AS"
"MS"
"""