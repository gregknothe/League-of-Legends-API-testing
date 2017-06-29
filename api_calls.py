import requests
import pandas
import os.path

##Goals:
#-Get each matches' data (mainly scores by time line (maybe each 5 minutes))
#-Create Win/Loss Dataframe to pull values from with external UI
#-Collect data in excel file (that can update when required)
#-Create UI to easily find statistics

def api_key():
    return "____________________________"


def fileLocation():
    #Location for your data to be saved.
    return "__________________________________________"


def user_id(userName, region="NA"):
    #Returns userID for other functions.
    userName = userName.lower()
    url = "https://na.api.riotgames.com/api/lol/" + region + "/v1.4/summoner/by-name/" + userName + "?api_key=" + api_key()
    try:
        json = requests.get(url)
        data = json.json()[userName]
    except:
        print "User does not exist."
        return 0
    return data['id']


def user_matches(userName, region="NA"):
    #Dataframe of matches played by user.
    id = user_id(userName, region)
    if id == 0:
        return 0
    try:
        url = "https://na.api.riotgames.com/api/lol/" + region + "/v2.2/matchlist/by-summoner/" + str(id) + "?api_key=" + api_key()
        json = requests.get(url)
        data = json.json()
    except:
        print "An error has occurred."
        return 0
    if data.keys()[0] == "matches":
        df = pandas.DataFrame.from_dict(data["matches"])
        return df
    else:
        return 0


def role(userName, region="NA"):
    #String of roles played in games.
    matches = user_matches(userName, region)
    df = pandas.DataFrame(matches, columns={"role", "lane"})
    role = []
    for i in range(len(df["role"])):
        if df["lane"][i] == "TOP":
            role.append("TOP")
        if df["lane"][i] == "JUNGLE":
            role.append("JUNGLE")
        if df["lane"][i] == "MID":
            role.append("MID")
        if df["lane"][i] == "BOTTOM" and df["role"][i] == "DUO_CARRY":
            role.append("CARRY")
        if df["lane"][i] == "BOTTOM" and df["role"][i] == "DUO_SUPPORT":
            role.append("SUPPORT")
    return role


def championID():
    #Gets champion ids from riot api.
    url = "http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json"
    json = requests.get(url)
    data = json.json()
    df = pandas.DataFrame.from_dict(data)
    champList = list(df.index)
    name = []
    id = []
    for i in champList:
        id.append(df["data"][i]["key"])
        name.append(i)
    champs = pandas.DataFrame({"name": name, "id": id})
    return champs


def matchLookUp(matchID):
    url = "https://na1.api.riotgames.com/lol/match/v3/matches/" + str(matchID) + "?api_key=" + api_key()
    json = requests.get(url)
    data = json.json()
    col = ["matchId", "season", "queueType", "patch", "mode", "duration", "startTime",

           "BlueWin", "BlueFirstInhib", "BlueRiftHerald", "BlueBaronKills", "BlueFirstTower", "BlueDragonKills",
           "BlueFirstBlood",

           "RedWin", "RedFirstInhib", "RedRiftHerald", "RedBaronKills", "RedFirstTower", "RedDragonKills",
           "RedFirstBlood",
           
           "Blue0Name", "Blue0Id", "Blue0Gold", "Blue0PinkWards", "Blue0DamageToObjectives", "Blue0WardsPlaced", "Blue0Kills",
           "Blue0Assists", "Blue0DamageToChampions", "Blue0Rank", "Blue0Lane", "Blue0Role", "Blue0GoldPerMin0-10", 
           "Blue0GoldPerMin10-20", "Blue0GoldPerMin20-30","Blue0GoldPerMin30-End", "Blue0CSPerMin0-10", "Blue0CSPerMin10-20", 
           "Blue0CSPerMin20-30", "Blue0CSPerMin30-End", "Blue0ChampionId",
           
           "Blue1Name", "Blue1Id", "Blue1Gold", "Blue1PinkWards", "Blue1DamageToObjectives", "Blue1WardsPlaced", "Blue1Kills", 
           "Blue1Assists","Blue1DamageToChampions", "Blue1Rank", "Blue1Lane", "Blue1Role", "Blue1GoldPerMin0-10", 
           "Blue1GoldPerMin10-20", "Blue1GoldPerMin20-30","Blue1GoldPerMin30-End", "Blue1CSPerMin0-10", "Blue1CSPerMin10-20", 
           "Blue1CSPerMin20-30", "Blue1CSPerMin30-End", "Blue1ChampionId",

           "Blue2Name", "Blue2Id", "Blue2Gold", "Blue2PinkWards", "Blue2DamageToObjectives", "Blue2WardsPlaced", "Blue2Kills",
           "Blue2Assists", "Blue2DamageToChampions", "Blue2Rank", "Blue2Lane", "Blue2Role", "Blue2GoldPerMin0-10",
           "Blue2GoldPerMin10-20", "Blue2GoldPerMin20-30", "Blue2GoldPerMin30-End", "Blue2CSPerMin0-10",
           "Blue2CSPerMin10-20", "Blue2CSPerMin20-30", "Blue2CSPerMin30-End", "Blue2ChampionId",

           "Blue3Name", "Blue3Id", "Blue3Gold",
           "Blue3PinkWards", "Blue3DamageToObjectives", "Blue3WardsPlaced", "Blue3Kills",
           "Blue3Assists", "Blue3DamageToChampions", "Blue3Rank", "Blue3Lane", "Blue3Role", "Blue3GoldPerMin0-10",
           "Blue3GoldPerMin10-20", "Blue3GoldPerMin20-30", "Blue3GoldPerMin30-End", "Blue3CSPerMin0-10",
           "Blue3CSPerMin10-20", "Blue3CSPerMin20-30", "Blue3CSPerMin30-End", "Blue3ChampionId",

           "Blue4Name", "Blue4Id", "Blue4Gold",
           "Blue4PinkWards", "Blue4DamageToObjectives", "Blue4WardsPlaced", "Blue4Kills",
           "Blue4Assists", "Blue4DamageToChampions", "Blue4Rank", "Blue4Lane", "Blue4Role", "Blue4GoldPerMin0-10",
           "Blue4GoldPerMin10-20", "Blue4GoldPerMin20-30", "Blue4GoldPerMin30-End", "Blue4CSPerMin0-10",
           "Blue4CSPerMin10-20", "Blue4CSPerMin20-30", "Blue4CSPerMin30-End", "Blue4ChampionId",

           "Red0Name", "Red0Id", "Red0Gold",
           "Red0PinkWards", "Red0DamageToObjectives", "Red0WardsPlaced", "Red0Kills",
           "Red0Assists", "Red0DamageToChampions", "Red0Rank", "Red0Lane", "Red0Role", "Red0GoldPerMin0-10",
           "Red0GoldPerMin10-20", "Red0GoldPerMin20-30", "Red0GoldPerMin30-End", "Red0CSPerMin0-10",
           "Red0CSPerMin10-20",
           "Red0CSPerMin20-30", "Red0CSPerMin30-End", "Red0ChampionId",

           "Red1Name", "Red1Id", "Red1Gold", "Red1PinkWards", "Red1DamageToObjectives", "Red1WardsPlaced",
           "Red1Kills",
           "Red1Assists", "Red1DamageToChampions", "Red1Rank", "Red1Lane", "Red1Role", "Red1GoldPerMin0-10",
           "Red1GoldPerMin10-20", "Red1GoldPerMin20-30", "Red1GoldPerMin30-End", "Red1CSPerMin0-10",
           "Red1CSPerMin10-20",
           "Red1CSPerMin20-30", "Red1CSPerMin30-End", "Red1ChampionId",

           "Red2Name", "Red2Id", "Red2Gold", "Red2PinkWards",
           "Red2DamageToObjectives", "Red2WardsPlaced", "Red2Kills",
           "Red2Assists", "Red2DamageToChampions", "Red2Rank", "Red2Lane", "Red2Role", "Red2GoldPerMin0-10",
           "Red2GoldPerMin10-20", "Red2GoldPerMin20-30", "Red2GoldPerMin30-End", "Red2CSPerMin0-10",
           "Red2CSPerMin10-20", "Red2CSPerMin20-30", "Red2CSPerMin30-End", "Red2ChampionId",

           "Red3Name", "Red3Id", "Red3Gold",
           "Red3PinkWards", "Red3DamageToObjectives", "Red3WardsPlaced", "Red3Kills",
           "Red3Assists", "Red3DamageToChampions", "Red3Rank", "Red3Lane", "Red3Role", "Red3GoldPerMin0-10",
           "Red3GoldPerMin10-20", "Red3GoldPerMin20-30", "Red3GoldPerMin30-End", "Red3CSPerMin0-10",
           "Red3CSPerMin10-20", "Red3CSPerMin20-30", "Red3CSPerMin30-End", "Red3ChampionId",

           "Red4Name", "Red4Id", "Red4Gold",
           "Red4PinkWards", "Red4DamageToObjectives", "Red4WardsPlaced", "Red4Kills",
           "Red4Assists", "Red4DamageToChampions", "Red4Rank", "Red4Lane", "Red4Role", "Red4GoldPerMin0-10",
           "Red4GoldPerMin10-20", "Red4GoldPerMin20-30", "Red4GoldPerMin30-End", "Red4CSPerMin0-10",
           "Red4CSPerMin10-20", "Red4CSPerMin20-30", "Red4CSPerMin30-End", "Red4ChampionId"
           ]

    values = [matchID, data.get("seasonId","NA"), data.get("gameType","NA"), data.get("gameVersion","NA"), data.get("gameMode","NA"),
             data.get("gameDuration","NA"), data.get("gameCreation","NA"),

             data["teams"][0]["win"], data["teams"][0]["firstInhibitor"], data["teams"][0]["firstRiftHerald"],
             data["teams"][0]["baronKills"], data["teams"][0]["firstTower"], data["teams"][0]["baronKills"],
             data["teams"][0]["firstBlood"],

             data["teams"][1]["win"], data["teams"][1]["firstInhibitor"], data["teams"][1]["firstRiftHerald"],
             data["teams"][1]["baronKills"], data["teams"][1]["firstTower"], data["teams"][1]["baronKills"],
             data["teams"][1]["firstBlood"],

             data["participantIdentities"][0]["player"]["summonerName"],
             data["participantIdentities"][0]["player"]["summonerId"], data["participants"][0]["stats"]["goldEarned"],
             data["participants"][0]["stats"]["visionWardsBoughtInGame"], data["participants"][0]["stats"]["damageDealtToObjectives"],
             data["participants"][0]["stats"]["wardsPlaced"], data["participants"][0]["stats"]["kills"], data["participants"][0]["stats"]["assists"],
             data["participants"][0]["stats"]["totalDamageDealtToChampions"], data["participants"][0]["highestAchievedSeasonTier"],
             data["participants"][0]["timeline"]["lane"], data["participants"][0]["timeline"]["role"],
             data["participants"][0]["timeline"]["goldPerMinDeltas"].get("0-10",0), data["participants"][0]["timeline"]["goldPerMinDeltas"].get("10-20",0),
             data["participants"][0]["timeline"]["goldPerMinDeltas"].get("20-30",0), data["participants"][0]["timeline"]["goldPerMinDeltas"].get("30-End",0),
             data["participants"][0]["timeline"]["creepsPerMinDeltas"].get("0-10",0), data["participants"][0]["timeline"]["creepsPerMinDeltas"].get("10-20",0),
             data["participants"][0]["timeline"]["creepsPerMinDeltas"].get("20-30",0), data["participants"][0]["timeline"]["creepsPerMinDeltas"].get("30-End",0),
             data["participants"][0]["championId"],

             data["participantIdentities"][1]["player"]["summonerName"],
             data["participantIdentities"][1]["player"]["summonerId"], data["participants"][1]["stats"]["goldEarned"],
             data["participants"][1]["stats"]["visionWardsBoughtInGame"],
             data["participants"][1]["stats"]["damageDealtToObjectives"],
             data["participants"][1]["stats"]["wardsPlaced"], data["participants"][1]["stats"]["kills"],
             data["participants"][1]["stats"]["assists"],
             data["participants"][1]["stats"]["totalDamageDealtToChampions"],
             data["participants"][1]["highestAchievedSeasonTier"],
             data["participants"][1]["timeline"]["lane"], data["participants"][1]["timeline"]["role"],
             data["participants"][1]["timeline"]["goldPerMinDeltas"].get("0-10",0),
             data["participants"][1]["timeline"]["goldPerMinDeltas"].get("10-20",0),
             data["participants"][1]["timeline"]["goldPerMinDeltas"].get("20-30",0),
             data["participants"][1]["timeline"]["goldPerMinDeltas"].get("30-End",0),
             data["participants"][1]["timeline"]["creepsPerMinDeltas"].get("0-10",0),
             data["participants"][1]["timeline"]["creepsPerMinDeltas"].get("10-20",0),
             data["participants"][1]["timeline"]["creepsPerMinDeltas"].get("20-30",0),
             data["participants"][1]["timeline"]["creepsPerMinDeltas"].get("30-End",0),
             data["participants"][1]["championId"],

              data["participantIdentities"][2]["player"]["summonerName"],
              data["participantIdentities"][2]["player"]["summonerId"], data["participants"][2]["stats"]["goldEarned"],
              data["participants"][2]["stats"]["visionWardsBoughtInGame"],
              data["participants"][2]["stats"]["damageDealtToObjectives"],
              data["participants"][2]["stats"]["wardsPlaced"], data["participants"][2]["stats"]["kills"],
              data["participants"][2]["stats"]["assists"],
              data["participants"][2]["stats"]["totalDamageDealtToChampions"],
              data["participants"][2]["highestAchievedSeasonTier"],
              data["participants"][2]["timeline"]["lane"], data["participants"][2]["timeline"]["role"],
              data["participants"][2]["timeline"]["goldPerMinDeltas"].get("0-10",0),
              data["participants"][2]["timeline"]["goldPerMinDeltas"].get("10-20",0),
              data["participants"][2]["timeline"]["goldPerMinDeltas"].get("20-30",0),
              data["participants"][2]["timeline"]["goldPerMinDeltas"].get("30-End",0),
              data["participants"][2]["timeline"]["creepsPerMinDeltas"].get("0-10",0),
              data["participants"][2]["timeline"]["creepsPerMinDeltas"].get("10-20",0),
              data["participants"][2]["timeline"]["creepsPerMinDeltas"].get("20-30",0),
              data["participants"][2]["timeline"]["creepsPerMinDeltas"].get("30-End",0),
              data["participants"][2]["championId"],

              data["participantIdentities"][3]["player"]["summonerName"],
              data["participantIdentities"][3]["player"]["summonerId"], data["participants"][3]["stats"]["goldEarned"],
              data["participants"][3]["stats"]["visionWardsBoughtInGame"],
              data["participants"][3]["stats"]["damageDealtToObjectives"],
              data["participants"][3]["stats"]["wardsPlaced"], data["participants"][3]["stats"]["kills"],
              data["participants"][3]["stats"]["assists"],
              data["participants"][3]["stats"]["totalDamageDealtToChampions"],
              data["participants"][3]["highestAchievedSeasonTier"],
              data["participants"][3]["timeline"]["lane"], data["participants"][3]["timeline"]["role"],
              data["participants"][3]["timeline"]["goldPerMinDeltas"].get("0-10",0),
              data["participants"][3]["timeline"]["goldPerMinDeltas"].get("10-20",0),
              data["participants"][3]["timeline"]["goldPerMinDeltas"].get("20-30",0),
              data["participants"][3]["timeline"]["goldPerMinDeltas"].get("30-End",0),
              data["participants"][3]["timeline"]["creepsPerMinDeltas"].get("0-10",0),
              data["participants"][3]["timeline"]["creepsPerMinDeltas"].get("10-20",0),
              data["participants"][3]["timeline"]["creepsPerMinDeltas"].get("20-30",0),
              data["participants"][3]["timeline"]["creepsPerMinDeltas"].get("30-End",0),
              data["participants"][3]["championId"],

              data["participantIdentities"][4]["player"]["summonerName"],
              data["participantIdentities"][4]["player"]["summonerId"], data["participants"][4]["stats"]["goldEarned"],
              data["participants"][4]["stats"]["visionWardsBoughtInGame"],
              data["participants"][4]["stats"]["damageDealtToObjectives"],
              data["participants"][4]["stats"]["wardsPlaced"], data["participants"][4]["stats"]["kills"],
              data["participants"][4]["stats"]["assists"],
              data["participants"][4]["stats"]["totalDamageDealtToChampions"],
              data["participants"][4]["highestAchievedSeasonTier"],
              data["participants"][4]["timeline"]["lane"], data["participants"][4]["timeline"]["role"],
              data["participants"][4]["timeline"]["goldPerMinDeltas"].get("0-10",0),
              data["participants"][4]["timeline"]["goldPerMinDeltas"].get("10-20",0),
              data["participants"][4]["timeline"]["goldPerMinDeltas"].get("20-30",0),
              data["participants"][4]["timeline"]["goldPerMinDeltas"].get("30-End",0),
              data["participants"][4]["timeline"]["creepsPerMinDeltas"].get("0-10",0),
              data["participants"][4]["timeline"]["creepsPerMinDeltas"].get("10-20",0),
              data["participants"][4]["timeline"]["creepsPerMinDeltas"].get("20-30",0),
              data["participants"][4]["timeline"]["creepsPerMinDeltas"].get("30-End",0),
              data["participants"][4]["championId"],

              data["participantIdentities"][5]["player"]["summonerName"],
              data["participantIdentities"][5]["player"]["summonerId"], data["participants"][5]["stats"]["goldEarned"],
              data["participants"][5]["stats"]["visionWardsBoughtInGame"],
              data["participants"][5]["stats"]["damageDealtToObjectives"],
              data["participants"][5]["stats"]["wardsPlaced"], data["participants"][5]["stats"]["kills"],
              data["participants"][5]["stats"]["assists"],
              data["participants"][5]["stats"]["totalDamageDealtToChampions"],
              data["participants"][5]["highestAchievedSeasonTier"],
              data["participants"][5]["timeline"]["lane"], data["participants"][5]["timeline"]["role"],
              data["participants"][5]["timeline"]["goldPerMinDeltas"].get("0-10",0),
              data["participants"][5]["timeline"]["goldPerMinDeltas"].get("10-20",0),
              data["participants"][5]["timeline"]["goldPerMinDeltas"].get("20-30",0),
              data["participants"][5]["timeline"]["goldPerMinDeltas"].get("30-End",0),
              data["participants"][5]["timeline"]["creepsPerMinDeltas"].get("0-10",0),
              data["participants"][5]["timeline"]["creepsPerMinDeltas"].get("10-20",0),
              data["participants"][5]["timeline"]["creepsPerMinDeltas"].get("20-30",0),
              data["participants"][5]["timeline"]["creepsPerMinDeltas"].get("30-End",0),
              data["participants"][5]["championId"],

              data["participantIdentities"][6]["player"]["summonerName"],
              data["participantIdentities"][6]["player"]["summonerId"], data["participants"][6]["stats"]["goldEarned"],
              data["participants"][6]["stats"]["visionWardsBoughtInGame"],
              data["participants"][6]["stats"]["damageDealtToObjectives"],
              data["participants"][6]["stats"]["wardsPlaced"], data["participants"][6]["stats"]["kills"],
              data["participants"][6]["stats"]["assists"],
              data["participants"][6]["stats"]["totalDamageDealtToChampions"],
              data["participants"][6]["highestAchievedSeasonTier"],
              data["participants"][6]["timeline"]["lane"], data["participants"][6]["timeline"]["role"],
              data["participants"][6]["timeline"]["goldPerMinDeltas"].get("0-10",0),
              data["participants"][6]["timeline"]["goldPerMinDeltas"].get("10-20",0),
              data["participants"][6]["timeline"]["goldPerMinDeltas"].get("20-30",0),
              data["participants"][6]["timeline"]["goldPerMinDeltas"].get("30-End",0),
              data["participants"][6]["timeline"]["creepsPerMinDeltas"].get("0-10",0),
              data["participants"][6]["timeline"]["creepsPerMinDeltas"].get("10-20",0),
              data["participants"][6]["timeline"]["creepsPerMinDeltas"].get("20-30",0),
              data["participants"][6]["timeline"]["creepsPerMinDeltas"].get("30-End",0),
              data["participants"][6]["championId"],

              data["participantIdentities"][7]["player"]["summonerName"],
              data["participantIdentities"][7]["player"]["summonerId"], data["participants"][7]["stats"]["goldEarned"],
              data["participants"][7]["stats"]["visionWardsBoughtInGame"],
              data["participants"][7]["stats"]["damageDealtToObjectives"],
              data["participants"][7]["stats"]["wardsPlaced"], data["participants"][7]["stats"]["kills"],
              data["participants"][7]["stats"]["assists"],
              data["participants"][7]["stats"]["totalDamageDealtToChampions"],
              data["participants"][7]["highestAchievedSeasonTier"],
              data["participants"][7]["timeline"]["lane"], data["participants"][7]["timeline"]["role"],
              data["participants"][7]["timeline"]["goldPerMinDeltas"].get("0-10",0),
              data["participants"][7]["timeline"]["goldPerMinDeltas"].get("10-20",0),
              data["participants"][7]["timeline"]["goldPerMinDeltas"].get("20-30",0),
              data["participants"][7]["timeline"]["goldPerMinDeltas"].get("30-End",0),
              data["participants"][7]["timeline"]["creepsPerMinDeltas"].get("0-10",0),
              data["participants"][7]["timeline"]["creepsPerMinDeltas"].get("10-20",0),
              data["participants"][7]["timeline"]["creepsPerMinDeltas"].get("20-30",0),
              data["participants"][7]["timeline"]["creepsPerMinDeltas"].get("30-End",0),
              data["participants"][7]["championId"],

              data["participantIdentities"][8]["player"]["summonerName"],
              data["participantIdentities"][8]["player"]["summonerId"], data["participants"][8]["stats"]["goldEarned"],
              data["participants"][8]["stats"]["visionWardsBoughtInGame"],
              data["participants"][8]["stats"]["damageDealtToObjectives"],
              data["participants"][8]["stats"]["wardsPlaced"], data["participants"][8]["stats"]["kills"],
              data["participants"][8]["stats"]["assists"],
              data["participants"][8]["stats"]["totalDamageDealtToChampions"],
              data["participants"][8]["highestAchievedSeasonTier"],
              data["participants"][8]["timeline"]["lane"], data["participants"][8]["timeline"]["role"],
              data["participants"][8]["timeline"]["goldPerMinDeltas"].get("0-10",0),
              data["participants"][8]["timeline"]["goldPerMinDeltas"].get("10-20",0),
              data["participants"][8]["timeline"]["goldPerMinDeltas"].get("20-30",0),
              data["participants"][8]["timeline"]["goldPerMinDeltas"].get("30-End",0),
              data["participants"][8]["timeline"]["creepsPerMinDeltas"].get("0-10",0),
              data["participants"][8]["timeline"]["creepsPerMinDeltas"].get("10-20",0),
              data["participants"][8]["timeline"]["creepsPerMinDeltas"].get("20-30",0),
              data["participants"][8]["timeline"]["creepsPerMinDeltas"].get("30-End",0),
              data["participants"][8]["championId"],

              data["participantIdentities"][9]["player"]["summonerName"],
              data["participantIdentities"][9]["player"]["summonerId"], data["participants"][9]["stats"]["goldEarned"],
              data["participants"][9]["stats"]["visionWardsBoughtInGame"],
              data["participants"][9]["stats"]["damageDealtToObjectives"],
              data["participants"][9]["stats"]["wardsPlaced"], data["participants"][9]["stats"]["kills"],
              data["participants"][9]["stats"]["assists"],
              data["participants"][9]["stats"]["totalDamageDealtToChampions"],
              data["participants"][9]["highestAchievedSeasonTier"],
              data["participants"][9]["timeline"]["lane"], data["participants"][9]["timeline"]["role"],
              data["participants"][9]["timeline"]["goldPerMinDeltas"].get("0-10",0),
              data["participants"][9]["timeline"]["goldPerMinDeltas"].get("10-20",0),
              data["participants"][9]["timeline"]["goldPerMinDeltas"].get("20-30",0),
              data["participants"][9]["timeline"]["goldPerMinDeltas"].get("30-End",0),
              data["participants"][9]["timeline"]["creepsPerMinDeltas"].get("0-10",0),
              data["participants"][9]["timeline"]["creepsPerMinDeltas"].get("10-20",0),
              data["participants"][9]["timeline"]["creepsPerMinDeltas"].get("20-30",0),
              data["participants"][9]["timeline"]["creepsPerMinDeltas"].get("30-End",0),
              data["participants"][9]["championId"]
              ]

    df = pandas.DataFrame(columns=col)
    df.loc[0] = values

    return df


def matchHistory(userName, region="NA"):
    if os.path.isfile(fileLocation()+ userName + ".csv") == False:
        matchIds = user_matches(userName, region)["matchId"]
        dataframe = matchLookUp(matchIds[0])
        for i in range(len(matchIds)-1):
            #print matchIds[i+1]
            try:
                data = matchLookUp(matchIds[i+1])
                dataframe = pandas.concat([dataframe, data])
                #dataframe.append(data, ignore_index=True)
            except:
                print "Match Done fucked up: " + str(matchIds[i+1])
        #print dataframe
        dataframe.to_csv(fileLocation() + userName + ".csv")
    else:
        fileData = pandas.read_csv(fileLocation() + userName + ".csv")
        matchIds = user_matches(userName, region)["matchId"]
        newMatchIds = list(set(matchIds)-set(fileData["matchIds"]))
        for i in range(len(newMatchIds)):
            try:
                data = matchLookUp(matchIds[i])
                fileData = pandas.concat([fileData, data])
            except:
                print "Match Done fucked up: " + str(matchIds[i+1])
            fileData.to_csv(fileLocation() + userName + ".csv")

    return
