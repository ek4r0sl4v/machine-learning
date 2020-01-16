import json
import string
import os
import sys
import glob

cwd = os.getcwd()

def findTeamAndReplaceWithBinaryCode(team, teamsArray, league):
    teamIndex = teamsArray.index(team)
    if (league == "Championship"):
        result = '{0:06b}'.format(teamIndex)
    else:
        result = '{0:05b}'.format(teamIndex)
    return result

def dayConversion(day):
    result = '{0:05b}'.format(day)
    return result
    
def monthConversion(month):
    result = '{0:04b}'.format(month)
    return result
    
def yearConversion(year):
    result = '{0:11b}'.format(year)
    return result

def replaceDateWithBinaryCode(date):
    binaryDate = []
    dateArray = date.split("/")
    binaryDay = dayConversion(int(dateArray[0]))
    binaryMonth = monthConversion(int(dateArray[1]))
    binaryYear = yearConversion(int(dateArray[2]))
    for x in binaryDay:
        binaryDate.append(x)
    for x in binaryMonth:
        binaryDate.append(x)
    for x in binaryYear:
        binaryDate.append(x)
    return binaryDate
 

def replaceResultWithBinary(matchResult, modelType):
    result = []
    if matchResult == "H":
        if modelType == "softmax":
            result = [1,0,0]
        else:
            result = 1
    elif matchResult == "A":
        if modelType == "softmax":
            result = [0,0,1]
        else:
            result = 0
    else:
        if modelType == "softmax":
            result = [0,1,0]
        else:
            result = 0.5
    return result

def replaceScore(teamGoals):
    result = [0,0,0,0,0,0]
    if(teamGoals >= 5):
        result[5] = 1
    else:
        result[teamGoals] = 1
    return result

    
def replacesScoreWithBinary(match, outputType, modelType):
    #print(str(match[3]) + ":" + str(match[4]))
    result = []
    if outputType == "scoreFT_v2":
        homeTeamFT = round(int(match[3])/10, 2)
        awayTeamFT = round(int(match[4])/10, 2)
        homeTeamHT = round(int(match[6])/10, 2)
        awayTeamHT = round(int(match[7])/10, 2)
    else:
        homeTeamFT = replaceScore(int(match[3]))
        awayTeamFT = replaceScore(int(match[4]))
        homeTeamHT = replaceScore(int(match[6]))
        awayTeamHT = replaceScore(int(match[7]))
    #print(homeTeamFT)
    #print(awayTeamFT)
    #print("--")
    resultFT = replaceResultWithBinary(match[5], modelType)
    resultHT = replaceResultWithBinary(match[8], modelType)
    
    if outputType == "onlyFT":
        if modelType == "softmax":
            for x in resultFT:
                result.append(int(x))
        elif modelType == "one":
            result.append(resultFT)
    elif outputType == "onlyHT":
        if modelType == "softmax":
            for x in resultHT:
                result.append(int(x))
        elif modelType == "one":
            result.append(resultHT)
    elif outputType == "FTHT":
        for x in resultFT:
            result.append(int(x))
        for x in resultHT:
            result.append(int(x))
            
    elif outputType == "scoreHome":
        for x in homeTeamFT:
            result.append(int(x))
    elif outputType == "scoreAway":

        for x in awayTeamFT:
            result.append(int(x))        
            
    elif outputType == "scoreFT":
        for x in homeTeamFT:
            result.append(int(x))
        for x in awayTeamFT:
            result.append(int(x))
    elif outputType == "scoreFT_v2":
        result.append(homeTeamFT)
        result.append(awayTeamFT)
    elif outputType == "scoreFTHT":
        for x in homeTeamFT:
            result.append(int(x))
        for x in awayTeamFT:
            result.append(int(x))
        for x in homeTeamHT:
            result.append(int(x))
        for x in awayTeamHT:
            result.append(int(x))
    elif outputType == "over3g":
        if int(match[3]) + int(match[4]) >= int(3):
            result = [1,0]
        else:
            result = [0,1]
    elif outputType == "over4g":
        if int(match[3]) + int(match[4]) >= int(4):  
            result.append(int(1))
        else:
            result.append(int(0))
    else:    
        for x in homeTeamFT:
            result.append(int(x))
        for x in awayTeamFT:
            result.append(int(x))
        result.append(resultFT)
        for x in homeTeamHT:
            result.append(int(x))
        for x in awayTeamHT:
            result.append(int(x))
        result.append(resultHT)
    #print(result)
    return result

def replacesScoreWithBinaryV2(match, outputType):
    result = []
    homeTeamFT = round(int(match[3])/10, 2)
    awayTeamFT = round(int(match[4])/10, 2)
    resultFT = replaceResultWithBinary(match[5])
    homeTeamHT = round(int(match[6])/10, 2)
    awayTeamHT = round(int(match[7])/10, 2)
    resultHT = replaceResultWithBinary(match[8])
    
    if outputType == "onlyFT":
        result.append(resultFT)
    elif outputType == "FTHT":
        result.append(resultFT)
        result.append(resultHT)
    elif outputType == "scoreFT":
        result.append(homeTeamFT)
        result.append(awayTeamFT)
    elif outputType == "scoreFTHT":
        result.append(homeTeamFT)
        result.append(awayTeamFT)
        result.append(homeTeamHT)
        result.append(awayTeamHT)
    else:    
        result.append(homeTeamFT)
        result.append(awayTeamFT)
        result.append(resultFT)
        result.append(homeTeamHT)
        result.append(awayTeamHT)
    #print(result)
    return result

def getMatchDataInput(match, teamsArray, league):
    result = []
    date = replaceDateWithBinaryCode(match[0])
    homeTeam = findTeamAndReplaceWithBinaryCode(match[1], teamsArray, league)
    awayTeam = findTeamAndReplaceWithBinaryCode(match[2], teamsArray, league)
    for x in date:
        result.append(int(x))
    for x in homeTeam:
        result.append(int(x))
    for x in awayTeam:
        result.append(int(x))
    return result

def getMatchWholeData(match, teamsArray, outputType, modelType, league):
    result = []
    input = getMatchDataInput(match, teamsArray, league)
    output = replacesScoreWithBinary(match, outputType, modelType)
    for x in input:
        result.append(x)
    for x in output:
        result.append(x)
    return result

def createAllTrainingData(newDataset, teams, league):
    finalDataset = []
    #datasetTypes = ["onlyFT", "FTHT", "scoreFT", "scoreFT_v2", "scoreFTHT","over3g","over4g" "all"]
    datasetTypes = ["onlyHT", "over3g", "onlyFT"]
    for modelType in ["softmax"]:
        for outputType in datasetTypes:
                for x in newDataset:
                    finalDataset.append(getMatchWholeData(x, teams, outputType, modelType, league))

                reverseFinalDataset = []
                length = len(finalDataset)
                #print(length)

                for i in range(0, length,1):
                    reverseFinalDataset.append(finalDataset[length - 1 - i])
    
                new_file_first = open(cwd + "/Football/Leagues/" + str(league) + "/" + str(league)+ ".txt", "w")
                #print(len(reverseFinalDataset))
                for item in reverseFinalDataset:
                    new_file_first.write("%s\n" % item)
                new_file_first.close()

                f1 = open(cwd + "/Football/Leagues/" + str(league) + "/" + str(league) + ".txt", 'r')
                f2 = open(cwd + "/Football/Leagues/" + str(league) + "/" + str(league) + "_" + str(outputType) + "_" + str(modelType) + ".txt", 'w')
                for line in f1:
                    f2.write(line.replace("[", "").replace("]",""))
                f1.close()
                f2.close()
                finalDataset = []

def createDatasetForPrediction(teams, league, fromLeagueRound, toLeagueRound):
    for y in range(fromLeagueRound, toLeagueRound):    
        A = []
        file = open(cwd + "/Football/Leagues/" + str(league) + "/" + league + "_upcomingMatches.csv", "r")
        for line in file:
            line = line.replace('\n', '')
            A.append(line)
        file.close()
        for i in range(len(A)):
            line = []
            newLine = []
            data = A[i].split(",")
            if(y == int(data[0])):
                for x in data:
                    line.append(x)
                date = replaceDateWithBinaryCode(line[1])
                homeTeam = findTeamAndReplaceWithBinaryCode(line[2], teams, league)
                awayTeam = findTeamAndReplaceWithBinaryCode(line[3], teams, league)
                for x in date:
                    newLine.append(int(x))
                for x in homeTeam:
                    newLine.append(int(x))
                for x in awayTeam:
                    newLine.append(int(x))
                #print(newLine)
                f1 = open(cwd + "/Football/Leagues/" + str(league) + "/" + league + "_" + "predictionDataset_" + str(y) + ".txt", "a")
                f1.write(str(newLine).replace("[", "").replace("]","") + '\n')
                f1.close()
                
def createDatasetForPredictionAccuracy(teams, league):  
    A = []
    file = open(cwd + "/Football/Leagues/" + str(league) + "/" + league + "_dataForResultsAcc.csv", "r")
    for line in file:
        line = line.replace('\n', '')
        A.append(line)
    file.close()
    for i in range(len(A)):
        line = []
        newLine = []
        data = A[i].split(",")
        for x in data:
            line.append(x)
        date = replaceDateWithBinaryCode(line[0])
        homeTeam = findTeamAndReplaceWithBinaryCode(line[1], teams, league)
        awayTeam = findTeamAndReplaceWithBinaryCode(line[2], teams, league)
        for x in date:
            newLine.append(int(x))
        for x in homeTeam:
            newLine.append(int(x))
        for x in awayTeam:
            newLine.append(int(x))
        #print(newLine)
        f1 = open(cwd + "/Football/Leagues/" + str(league) + "/" + league + "_" + "predictionAccuracyDataset" + ".txt", "a")
        f1.write(str(newLine).replace("[", "").replace("]","") + '\n')
        f1.close()            
            

def createDatasetAndTeams(league):
    A = []
    file = open(cwd + "/Football/Leagues/" + str(league) + "/" + str(league) + ".csv", "r")
    for line in file:
        line = line.replace('\n', '')
        A.append(line)
    file.close()
    A.pop(0)
    newDataset = []
    teams = []
    for i in range(len(A)):
        line = []
        newLine = []
        data = A[i].split(",")
        for x in data:
            line.append(x)
        for y in range(1, 10):
            if y == 2:
                try:
                    index = teams.index(line[y])
                except ValueError:
                    index = "null"
                if type(index) is str:
                    teams.append(line[y])

            if y == 3:
                try:
                    index = teams.index(line[y])
                except ValueError:
                    index = "null"
                if type(index) is str:
                    teams.append(line[y])
            newLine.append(line[y])
        newDataset.append(newLine)
    file_teams = open(cwd + "/Football/Leagues/" + str(league) + "/" + league + "_teams.txt", "w")
    
    for i in range (len(teams)):
        #print(teams[i])
        file_teams.write(teams[i] + "\n")
    #print(len(teams))
    createAllTrainingData(newDataset, teams, league)
    #number is league round
    createDatasetForPrediction(teams, league, 7, 20)
    createDatasetForPredictionAccuracy(teams, league)

def deleteAllFiles():
    fileList = glob.glob(cwd + "\Football\Leagues\*\*.txt", recursive=True)
    for filePath in fileList:
        #print(filePath)
        try:
            os.remove(filePath)
        except OSError:
            print("Error while deleting file")
    print("All files deleted.")

def main():
    if (sys.argv[1] == "delete"):
        # delete all old files
        deleteAllFiles()
    elif (sys.argv[1] == "create"):
        # create new files
        leagues = ["Bundesliga", "Championship", "LaLigue", "PremierLeague"]
        for league in leagues:
            createDatasetAndTeams(league)
        print("Datasets created.")

if __name__ == "__main__":
    main()