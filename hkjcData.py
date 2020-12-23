import json
from contentLoader import *

baseURL = 'https://bet.hkjc.com/football/getJSON.aspx?jsontype=odds_allodds.aspx'

#get the avaliable matches list
def getMatchList():
    r = contentLoader(baseURL)
    j = json.loads(r.text)
    ret = {
        "count": 0,
        "item": []
        }
    for match in j:
        ret["count"] += 1
        ret["item"].append({
            "index": ret["count"],
            "matchID": match["matchID"],
            "matchIDinofficial": match["matchIDinofficial"],
            "matchTime": match["matchTime"],
            "matchNum": match["matchNum"],
            "matchDay": match["matchDay"],
            "matchID": match["matchID"],
            "hometeamNameCH": match["homeTeam"]["teamNameCH"],
            "hometeamNameEN": match["homeTeam"]["teamNameEN"],
            "awayteamNameCH": match["awayTeam"]["teamNameCH"],
            "awayteamNameEN": match["awayTeam"]["teamNameEN"],
            })
    return ret;

#convert the internal index to HKJC match ID
def indexToMatchId(index,matches):
    for match in matches["item"]:
        if(int(match["index"]) == int(index)):
            return match["matchID"]
    return None

def printPrettyJSON(parsed):
    print(json.dumps(parsed, indent=4, sort_keys=True))

#get information for single match
def getMatchJSON(matchId):
    reqeustUrl = baseURL+"&matchid="+matchId
    r = contentLoader(reqeustUrl)
    j = json.loads(r.text)
    target = None
    for match in j:
        if(match["matchID"] == matchId):
            target = match
            break
    return target

    
def main():
    matches = getMatchList()
    for match in matches["item"]:
        tbp = str(match["index"])+"\t"+match["matchDay"]+match["matchNum"]+" "+match["hometeamNameCH"]+" vs "+match["awayteamNameCH"]+"\t\t"+ match["matchID"]+"\n"
        print(tbp)
    while True:
        index = int(input("Please select a match: "))
        if index == -1:
            break
        print(json.dumps(getMatchJSON(indexToMatchId(index,matches)), indent=4, sort_keys=True))
        
if __name__ == '__main__':
    main()
