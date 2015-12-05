### ========================================================= ###
###                      IMPORT PACKAGES                      ### 
### ========================================================= ###

import re
import urllib2
import csv
from BeautifulSoup import BeautifulSoup
import math
import datetime
from dateutil import parser

### ========================================================= ###
###                   INITIALIZE VARIABLES                    ### 
### ========================================================= ###

count = -1
OutputData = list()
kicker_list = list()
soup = list()
tags = list()
teams = list()
weeks = list()
months = list()
months = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
headings = list()
headings = ('player','position','team','opponent','date','location','cmp','pass_att','pass_yd','pass_td','int_thrown','pass_long','rush_att','rush_yd','rush_td','rush_long','targets','receptions','rec_yd','rec_td','rec_long','fumbles','fumbles_lost','int_made','int_yds','int_td','int_long','sacks','tackles','ast','fumbles_recovered','fum_yds','fum_rec_td','forced_fumbles','safeties','kick_ret','kick_ret_yds','yds_per_kick_ret','kick_ret_td','kick_ret_long','punt_ret','punt_ret_yds','yds_per_punt_ret','punt_ret_td','punt_ret_lng','xpm','xpa','fgm','fga','fg_made_lengths','fg_missed_lengths','off_snap_count','off_snap_count_pct','def_snap_count','def_snap_count_pct','st_snap_count','st_snap_count_pct','fantasy_points','qbr','two_pt_conv','pts_allowed','season','week')
data = dict()
locations = dict()
locations = {'Baltimore Ravens':'BAL','Cincinnati Bengals':'CIN','Cleveland Browns':'CLE','Pittsburgh Steelers':'PIT','Houston Texans':'HOU','Indianapolis Colts':'IND','Jacksonville Jaguars':'JAX','Tennessee Titans':'TEN','Buffalo Bills':'BUF','Miami Dolphins':'MIA','New England Patriots':'NWE','New York Jets':'NYJ','Denver Broncos':'DEN','Kansas City Chiefs':'KAN','Oakland Raiders':'OAK','San Diego Chargers':'SDG','Chicago Bears':'CHI','Detroit Lions':'DET','Green Bay Packers':'GNB','Minnesota Vikings':'MIN','Atlanta Falcons':'ATL','Carolina Panthers':'CAR','New Orleans Saints':'NOR','Tampa Bay Buccaneers':'TAM','Dallas Cowboys':'DAL','New York Giants':'NYG','Philadelphia Eagles':'PHI','Washington Redskins':'WAS','Arizona Cardinals':'ARI','San Francisco 49ers':'SFO','Seattle Seahawks':'SEA','St. Louis Rams':'STL'}
positionList = list()
positionList = ('QB', 'WR', 'RB', 'TE', 'FB')
otherPlayers = dict()
otherPlayers = {'Austin Davis':'QB','Chris Cook':'CB','Drew Davis':'WR','Josh Johnson':'QB','Mike Jenkins':'CB','Damien Williams':'RB','John Brown':'WR','Tre Mason':'RB'}

### ========================================================= ###
###                      FUNCTIONS                            ### 
### ========================================================= ###

def OffenseStats(text, startPos, endPos, date):

    global teams
    global year

    # Initialize variables
    teams = list()
    initialStart = startPos
    count = 4
    
    tag_count = text[startPos:endPos].count("</tr>")
    
    while (count < tag_count) and (startPos >= initialStart):
        count += 1
        try:
            playerDict = dict()        
            
            # Find the name of the player
            playerStart = text.find(".htm", startPos, endPos) + 6
            playerEnd = text.find("</a>", playerStart, endPos)
            player = text[playerStart:playerEnd]
    
            # Initialize the structure of the player dictionary
            playerDict = {'position':0,'team':0,'opponent':0,'location':0,'cmp':0,'pass_att':0,'pass_yd':0,'pass_td':0,'int_thrown':0,'pass_long':0,'rush_att':0,'rush_yd':0,'rush_td':0,'rush_long':0,'targets':0,'receptions':0,'rec_yd':0,'rec_td':0,'rec_long':0,'fumbles':0,'fumbles_lost':0,'int_made':0,'int_yds':0,'int_td':0,'int_long':0,'sacks':0.0,'tackles':0,'ast':0,'fumbles_recovered':0,'fum_yds':0,'fum_rec_td':0,'forced_fumbles':0,'safeties':0,'kick_ret':0,'kick_ret_yds':0,'yds_per_kick_ret':0,'kick_ret_td':0,'kick_ret_long':0,'punt_ret':0,'punt_ret_yds':0,'yds_per_punt_ret':0,'punt_ret_td':0,'punt_ret_lng':0,'xpm':0,'xpa':0,'fgm':0,'fga':0,'fg_made_lengths':0,'fg_missed_lengths':0,'off_snap_count':0,'off_snap_count_pct':0,'def_snap_count':0,'def_snap_count_pct':0,'st_snap_count':0,'st_snap_count_pct':0,'fantasy_points':0,'qbr':0,'two_pt_conv':0,'pts_allowed':0,'season':year + 2000,'week':0}
            data[date][player] = playerDict

            # Find the team the player plays for during that game
            teamStart = text.find("csk=\"", playerEnd, endPos) + 8
            teamEnd = text.find("</td>", teamStart, endPos)
            team = text[teamStart:teamEnd]
            data[date][player]['team'] = team
    
            # Append team name to teams list to be referenced later when determining who opponent is
            if team not in teams:
                teams.append(team)
    
            # Return metrics from box score
            for m in range(0, 17):
                if m == 0:
                    metricStart = playerEnd + 50
                    metricEnd = text.find("</td>", metricStart, endPos)
                else:
                    metricStart = metricEnd + 5
                    metricEnd = text.find("</td>", metricStart - 1, endPos)
                
                metricStart = text.find(">", metricEnd - 7, metricEnd) + 1
    
                # Append values for only those metrics that are shown in the box score (ignore nulls)
                if metricEnd - metricStart > 0:
                    data[date][player][headings[m + 6]] = text[metricStart:metricEnd]
                
            # Increase start Pos to find new player
            startPos = text.find("</tr>", metricEnd, len(text))
            
        except:
            continue
            
    return


def ReturnStats(text, startPos, endPos, date):

    global year
        
    # Initialize variables
    initialStart = startPos
    count = 4
    
    tag_count = text[startPos:endPos].count("</tr>")
    
    while (count < tag_count) and (startPos >= initialStart):
        count += 1
        try:
            playerStart = text.find(".htm", startPos, endPos) + 6
            playerEnd = text.find("</a>", playerStart, endPos)
            player = text[playerStart:playerEnd]
            
            # Check if this player already exists in the dictionary.  If not, create record.
            if player not in data[date]:
                
                # Find the team the player plays for during that game
                teamStart = text.find("csk=\"", playerEnd, endPos) + 8
                teamEnd = text.find("</td>", teamStart, endPos)
                team = text[teamStart:teamEnd]

                # Create the dictionary entry for that player
                playerdict = dict()
                playerdict = {'position':0,'team':team,'opponent':0,'location':0,'cmp':0,'pass_att':0,'pass_yd':0,'pass_td':0,'int_thrown':0,'pass_long':0,'rush_att':0,'rush_yd':0,'rush_td':0,'rush_long':0,'targets':0,'receptions':0,'rec_yd':0,'rec_td':0,'rec_long':0,'fumbles':0,'fumbles_lost':0,'int_made':0,'int_yds':0,'int_td':0,'int_long':0,'sacks':0.0,'tackles':0,'ast':0,'fumbles_recovered':0,'fum_yds':0,'fum_rec_td':0,'forced_fumbles':0,'safeties':0,'kick_ret':0,'kick_ret_yds':0,'yds_per_kick_ret':0,'kick_ret_td':0,'kick_ret_long':0,'punt_ret':0,'punt_ret_yds':0,'yds_per_punt_ret':0,'punt_ret_td':0,'punt_ret_lng':0,'xpm':0,'xpa':0,'fgm':0,'fga':0,'fg_made_lengths':0,'fg_missed_lengths':0,'off_snap_count':0,'off_snap_count_pct':0,'def_snap_count':0,'def_snap_count_pct':0,'st_snap_count':0,'st_snap_count_pct':0,'fantasy_points':0,'qbr':0,'two_pt_conv':0,'pts_allowed':0,'season':year + 2000,'week':0}
                data[date][player] = playerdict
        
            # Return metrics from box score
            for m in range(0, 10):
                if m ==0:
                    metricStart = playerEnd + 50
                    metricEnd = text.find("</td>", metricStart, endPos)
                else:
                    metricStart = metricEnd + 5
                    metricEnd = text.find("</td>", metricStart, endPos)
                    
                metricStart = text.find(">", metricEnd - 7, metricEnd) + 1
    
                # Append values for only those metrics that are shown in the box score (ignore nulls)
                if metricEnd - metricStart > 0:
                    data[date][player][headings[m + 35]] = text[metricStart:metricEnd]
                
            # Increase start Pos to find new player
            startPos = text.find("</tr>", metricEnd, len(text))        
        
        except:
            continue

    return

def DefenseStats(text, startPos, endPos, date):

    global defense_dict
    global teams
    global locations
            
    initialStart = startPos
    count = 4
    
    tag_count = text[startPos:endPos].count("</tr>")
    
    defense_dict = dict()
    for team in teams:
        defense_dict[team] = dict()
        defense_dict[team] = {'def_snap_count':0,'def_snap_count_pct':0}
    
    while (count < tag_count) and (startPos >= initialStart):
        count += 1
        try:
            # Find starting position for player
            playerStart = text.find(".htm", startPos, endPos) + 6
            playerEnd = text.find("</a>", playerStart, endPos)
            player = text[playerStart:playerEnd]
            
            # Find the team the player plays for during that game
            teamStart = text.find("csk=\"", playerEnd, endPos) + 8
            teamEnd = text.find("</td>", teamStart, endPos)
            team = text[teamStart:teamEnd]

            # Append player to defense dictionary for use later
            defense_dict[team][player] = 0
            
            # Change player variable so that all stats are added up under a single defense
            player = str(team) + " Defense"
        
            # Return defense metrics from box score
            for m in range(0, 11):
                metricValue = 0
                if m ==0:
                    metricStart = playerEnd + 50
                    metricEnd = text.find("</td>", metricStart, endPos)
                else:
                    metricStart = metricEnd + 5
                    metricEnd = text.find("</td>", metricStart, endPos)

                metricStart = text.find(">", metricEnd - 7, metricEnd) + 1
    
                # Append values for only those metrics that are shown in the box score (ignore nulls)
                if metricEnd - metricStart > 0:
                    metricValue = float(text[metricStart:metricEnd])
                    data[date][player][headings[m + 23]] += metricValue
    
            # Increase start Pos to find next player
            startPos = text.find("</tr>", metricEnd, len(text))
        
        except:
            continue

    # Add individual player return stats into defense stats
    for player in data[date]:
        if player[-8:] <> " Defense":
            if int(data[date][player]['kick_ret_td']) > 0:
                team = data[date][player]['team']
                data[date][team + " Defense"]['kick_ret_td'] += int(data[date][player]['kick_ret_td'])
            if int(data[date][player]['punt_ret_td']) > 0:
                team = data[date][player]['team']
                data[date][team + " Defense"]['punt_ret_td'] += int(data[date][player]['punt_ret_td'])

    # Add safeties
    if text.count("Safety") > 0:
        startPos = text.find("Safety", 0, len(text)) - 32
        startPos = text.find("</td><td>", startPos, len(text)) + 9
        endPos = text.find("</td><td>", startPos, len(text))
        team = text[startPos:endPos]
        for l in locations:
            if team in l:
                team = locations[l] + " Defense"
                break
        data[date][team]['safeties'] = 1
    
    return

def KickerStats(text, startPos, endPos, date):

    global kicker_list
    global year

    count = 4
    initialStart = startPos
    
    tag_count = text[startPos:endPos].count("</tr>")

    while (count < tag_count) and (startPos >= initialStart):
        count += 1
        # Find starting position for player
        playerStart = text.find(".htm", startPos, endPos) + 6
        playerEnd = text.find("</a>", playerStart, endPos)
        player = text[playerStart:playerEnd]

        # Proceed if the player is a kicker
        if player in kicker_list:

            # Find the team the player plays for during that game
            teamStart = text.find("csk=\"", playerEnd, endPos) + 8
            teamEnd = text.find("</td>", teamStart, endPos)
            team = text[teamStart:teamEnd]

            if player not in data[date]:
                playerdict = dict()
                playerdict = {'position':'K','team':0,'opponent':0,'location':0,'cmp':0,'pass_att':0,'pass_yd':0,'pass_td':0,'int_thrown':0,'pass_long':0,'rush_att':0,'rush_yd':0,'rush_td':0,'rush_long':0,'targets':0,'receptions':0,'rec_yd':0,'rec_td':0,'rec_long':0,'fumbles':0,'fumbles_lost':0,'int_made':0,'int_yds':0,'int_td':0,'int_long':0,'sacks':0.0,'tackles':0,'ast':0,'fumbles_recovered':0,'fum_yds':0,'fum_rec_td':0,'forced_fumbles':0,'safeties':0,'kick_ret':0,'kick_ret_yds':0,'yds_per_kick_ret':0,'kick_ret_td':0,'kick_ret_long':0,'punt_ret':0,'punt_ret_yds':0,'yds_per_punt_ret':0,'punt_ret_td':0,'punt_ret_lng':0,'xpm':0,'xpa':0,'fgm':0,'fga':0,'fg_made_lengths':0,'fg_missed_lengths':0,'off_snap_count':0,'off_snap_count_pct':0,'def_snap_count':0,'def_snap_count_pct':0,'st_snap_count':0,'st_snap_count_pct':0,'fantasy_points':0,'qbr':0,'two_pt_conv':0,'pts_allowed':0,'season':year + 2000,'week':0}
                data[date][player] = playerdict

            # Append team name
            data[date][player]['team'] = team

            # Return metrics from box score
            for m in range(0, 4):
                if m == 0:
                    metricStart = playerEnd + 50
                    metricEnd = text.find("</td>", metricStart, endPos)
                else:
                    metricStart = metricEnd + 5
                    metricEnd = text.find("</td>", metricStart, endPos)
                    
                metricStart = text.find(">", metricEnd - 7, metricEnd) + 1
                
                # Append values for only those metrics that are shown in the box score (ignore nulls)
                if metricEnd - metricStart > 0:
                    data[date][player][headings[m + 45]] = text[metricStart:metricEnd]

            # Increase start Pos to find next player
            startPos = text.find("</tr>", metricEnd, len(text))
        
        else:
            startPos = text.find("</tr>", playerEnd + 100, len(text))

    # Append lengths of kicks made and missed to dictionary
    startPos = text.find("Passing, Rushing")
    text = text[startPos:len(text)]
    
    kicker_dict = dict()
    fg = list()
    fg = ('field goal good. Penalty', 'field goal good<', 'field goal no good, ', 'field goal no good<', 'field goal no good. ')
    
    for f in fg:
        count = 0
        fg_length = 0
        fg_count = text.count(f)
        fg_start = text.find(f)
        if f == 'field goal good<' or f == 'field goal good. Penalty':
            key = 'fg_made_lengths'
        else:
            key = 'fg_missed_lengths'
        while count < fg_count:
            fg_length = 0
            count += 1
            if count > 1:
                fg_start = text.find(f, endPos + 50, len(text))
            startPos = text.find(".htm", fg_start - 50) + 6
            endPos = text.find("</a>", startPos, fg_start)
            player = text[startPos:endPos]
            if player not in kicker_dict:
                kicker_dict[player] = {'fg_made_lengths':list(),'fg_missed_lengths':list()}
            if (f == 'field goal good. Penalty') and (text[fg_start:fg_start + 250].count('(no play)') == 0):
                fg_length = text[fg_start - 8:fg_start - 6]
            elif ((f == 'field goal good<') or (f == 'field goal no good, ') or (f == 'field goal no good<') or (f == 'field goal no good. ')) and (text[fg_start:fg_start + 300].count('(no play)') == 0):
                fg_length = text[fg_start - 8:fg_start - 6]
            if (fg_length > 0) and (fg_length <> None):
                kicker_dict[player][key].append(fg_length)
            if (player in kicker_dict) and (len(kicker_dict[player][key])) > 0:
                data[date][player][key] = kicker_dict[player][key]
    
    return


def Opponents(date):
    
    global teams

    for curPlayer in data[date]:
        if data[date][curPlayer]['team'] == teams[0] and len(teams) == 2:
            data[date][curPlayer]['opponent'] = teams[1]
        elif data[date][curPlayer]['team'] == teams[1] and len(teams) == 2:
            data[date][curPlayer]['opponent'] = teams[0]

def TwoPtConv(text, date):
    
    count = 0
    pcount = 0
    playerList = list()
    startPos = text.find("Passing, Rushing")
    text = text[startPos:len(text)]
    conversion_count = text.count("conversion succeeds")
    
    if conversion_count > 0:
        conversion_start = text.find("conversion succeeds")
    
    while count < conversion_count:
        count += 1
        player_count = text.count(".htm", conversion_start - 150, conversion_start)
        pcount = 0
        while pcount < player_count:
            pcount += 1
            if (count == 1) and (pcount == 1):
                startPos = text.find(".htm", conversion_start - 300, conversion_start) + 6
                endPos = text.find("</a>", startPos, conversion_start)
            elif pcount > 1:
                startPos = text.find(".htm", endPos + 1, conversion_start) + 6
                endPos = text.find("</a>", startPos, conversion_start)
            elif (count > 1) and (pcount == 1):
                conversion_start = text.find("conversion succeeds", endPos + 100, len(text))
                startPos = text.find(".htm", conversion_start - 300, conversion_start) + 6
                endPos = text.find("</a>", startPos, conversion_start)
            playerList.append(text[startPos:endPos])
        conversion_start = text.find("conversion succeeds", conversion_start + 20, len(text))
        
    for player in playerList:
        if player not in data[date]:
            playerdict = dict()
            playerdict = {'position':0,'team':0,'opponent':0,'location':0,'cmp':0,'pass_att':0,'pass_yd':0,'pass_td':0,'int_thrown':0,'pass_long':0,'rush_att':0,'rush_yd':0,'rush_td':0,'rush_long':0,'targets':0,'receptions':0,'rec_yd':0,'rec_td':0,'rec_long':0,'fumbles':0,'fumbles_lost':0,'int_made':0,'int_yds':0,'int_td':0,'int_long':0,'sacks':0.0,'tackles':0,'ast':0,'fumbles_recovered':0,'fum_yds':0,'fum_rec_td':0,'forced_fumbles':0,'safeties':0,'kick_ret':0,'kick_ret_yds':0,'yds_per_kick_ret':0,'kick_ret_td':0,'kick_ret_long':0,'punt_ret':0,'punt_ret_yds':0,'yds_per_punt_ret':0,'punt_ret_td':0,'punt_ret_lng':0,'xpm':0,'xpa':0,'fgm':0,'fga':0,'fg_made_lengths':0,'fg_missed_lengths':0,'off_snap_count':0,'off_snap_count_pct':0,'def_snap_count':0,'def_snap_count_pct':0,'st_snap_count':0,'st_snap_count_pct':0,'fantasy_points':0,'qbr':0,'two_pt_conv':0,'pts_allowed':0,'season':year + 2000,'week':0}
            data[date][player] = playerdict
        data[date][player]['two_pt_conv'] += 1
        
    return


def Qbr(completions, attempts, yards, touchdowns, interceptions):
    try:
        a = ((completions/attempts) - 0.3)*5
        b = ((yards/attempts) - 3)*0.25
        c = (touchdowns/attempts)*20
        d = 2.375 - (interceptions*25/attempts)
        
        y = round(100*(a + b + c + d)/6, 2)

        if y > 158.3:
            y = 158.3
        elif y < 0:
            y = 0
        
    except:
        y = 0
        
    return y


def Positions(text, startPos, endPos, date):

    global teams
    global defense_dict
    global kicker_list
    global year
    global positionList
    global otherPlayers
    
    count = 4
    initialStart = startPos
    
    tag_count = text[startPos:endPos].count("</tr>")
    
    
    while (count < tag_count) and (startPos >= initialStart):
        count += 1
        try:
            # Find the name of the player
            playerStart = text.find(".htm", startPos, endPos) + 6
            playerEnd = text.find("</a>", playerStart, endPos)
            player = text[playerStart:playerEnd]

            # Find the kickers for lookup later
            if (player not in data[date]):
                metricStart = playerEnd + 5
                metricEnd = text.find("</td>", metricStart, endPos)
                metricStart = text.find(">", metricEnd - 8, metricEnd) + 1
                position = text[metricStart:metricEnd]
                if (position == 'K') and (player not in kicker_list):
                    kicker_list.append(player)
                    playerdict = dict()
                    playerdict = {'position':'K','team':0,'opponent':0,'location':0,'cmp':0,'pass_att':0,'pass_yd':0,'pass_td':0,'int_thrown':0,'pass_long':0,'rush_att':0,'rush_yd':0,'rush_td':0,'rush_long':0,'targets':0,'receptions':0,'rec_yd':0,'rec_td':0,'rec_long':0,'fumbles':0,'fumbles_lost':0,'int_made':0,'int_yds':0,'int_td':0,'int_long':0,'sacks':0.0,'tackles':0,'ast':0,'fumbles_recovered':0,'fum_yds':0,'fum_rec_td':0,'forced_fumbles':0,'safeties':0,'kick_ret':0,'kick_ret_yds':0,'yds_per_kick_ret':0,'kick_ret_td':0,'kick_ret_long':0,'punt_ret':0,'punt_ret_yds':0,'yds_per_punt_ret':0,'punt_ret_td':0,'punt_ret_lng':0,'xpm':0,'xpa':0,'fgm':0,'fga':0,'fg_made_lengths':0,'fg_missed_lengths':0,'off_snap_count':0,'off_snap_count_pct':0,'def_snap_count':0,'def_snap_count_pct':0,'st_snap_count':0,'st_snap_count_pct':0,'fantasy_points':0,'qbr':0,'two_pt_conv':0,'pts_allowed':0,'season':year + 2000,'week':0}
                    data[date][player] = playerdict
            
            # Make sure the player exists in the data.  If not (probably because he's an offensive tackle or defensive player), move on to next player
            if player in data[date]:
                
                for m in range(0, 7):
                    if m == 0:
                        metricStart = playerEnd + 20
                        metricEnd = text.find("</td>", metricStart, endPos)
                    if m > 0:
                        metricStart = metricEnd + 5
                        metricEnd = text.find("</td>", metricStart, endPos)
                        
                    metricStart = text.find(">", metricEnd - 8, metricEnd) + 1

                    # Find the player position and append it to the dictionary
                    if m == 0:
                        position = text[metricStart:metricEnd]

                        # Append position to dictionary
                        if player in data[date]:
                            data[date][player]['position'] = position
                        # Some players may have played but not done accumulated any yards.  Include these as well.
                        elif position in positionList:
                            playerdict = dict()
                            playerdict = {'position':position,'team':0,'opponent':0,'location':0,'cmp':0,'pass_att':0,'pass_yd':0,'pass_td':0,'int_thrown':0,'pass_long':0,'rush_att':0,'rush_yd':0,'rush_td':0,'rush_long':0,'targets':0,'receptions':0,'rec_yd':0,'rec_td':0,'rec_long':0,'fumbles':0,'fumbles_lost':0,'int_made':0,'int_yds':0,'int_td':0,'int_long':0,'sacks':0.0,'tackles':0,'ast':0,'fumbles_recovered':0,'fum_yds':0,'fum_rec_td':0,'forced_fumbles':0,'safeties':0,'kick_ret':0,'kick_ret_yds':0,'yds_per_kick_ret':0,'kick_ret_td':0,'kick_ret_long':0,'punt_ret':0,'punt_ret_yds':0,'yds_per_punt_ret':0,'punt_ret_td':0,'punt_ret_lng':0,'xpm':0,'xpa':0,'fgm':0,'fga':0,'fg_made_lengths':0,'fg_missed_lengths':0,'off_snap_count':0,'off_snap_count_pct':0,'def_snap_count':0,'def_snap_count_pct':0,'st_snap_count':0,'st_snap_count_pct':0,'fantasy_points':0,'qbr':0,'two_pt_conv':0,'pts_allowed':0,'season':year + 2000,'week':0}
                            data[date][player] = playerdict
                            
                    # Append snap counts to the dictionary
                    elif (m > 0) and (metricEnd - metricStart > 0):
                        data[date][player][headings[m + 50]] = text[metricStart:metricEnd]

            # Try to find total number of defense snaps for that team
            for team in teams:
                if (player in defense_dict[team]):
                    for m in range(0, 5):
                        if m ==0:
                            metricStart = playerEnd + 20
                            metricEnd = text.find("</td>", metricStart, endPos)
                        else:
                            metricStart = metricEnd + 5
                            metricEnd = text.find("</td>", metricStart, endPos)
                        
                        metricStart = text.find(">", metricEnd - 8, metricEnd) + 1

                        if m == 3:
                            metric = int(text[metricStart:metricEnd])
                            if metric > defense_dict[team]['def_snap_count']:
                                defense_dict[team]['def_snap_count'] = metric
                        elif m == 4:
                            metric = int(text[metricStart:metricEnd - 1])
                            if metric > defense_dict[team]['def_snap_count_pct']:
                                defense_dict[team]['def_snap_count_pct'] = metric
                
            # Increase start text Pos to find new player
            startPos = text.find("</tr>", playerEnd, len(text))

        except:
            continue
            
    # Add defense snap metrics to defenses
    for team in teams:
        player = str(team) + " Defense"
        data[date][player]['def_snap_count_pct'] = "100%"
        if defense_dict[team]['def_snap_count'] > 0:
            data[date][player]['def_snap_count'] = 100 * defense_dict[team]['def_snap_count'] / defense_dict[team]['def_snap_count_pct']
        else:
            data[date][player]['def_snap_count'] = defense_dict[team]['def_snap_count']
        
    return


def FantasyPoints(date, player, position, pass_yd, pass_td, int_thrown, rush_yd, rush_td, rec_yd, rec_td, fumbles_lost, int_made, int_td, sacks, fumbles_recovered, fum_rec_td, safeties, kick_ret_td, punt_ret_td, two_pt_conv, pts_allowed, xpm, xpa, fgm, fga, fg_lengths):
    
    if position == 'K':
        lengthPts = 0
        if fg_lengths <> 0:
            for length in fg_lengths:
                if int(length) < 40:
                    lengthPts += 3
                elif int(length) < 50:
                    lengthPts += 4
                else:
                    lengthPts += 5            
        totalPts = xpm - (xpa - xpm) - (fga - fgm) + lengthPts
        
    else: 
        d = 0
        passPts = math.floor(pass_yd/25) + pass_td*4 - int_thrown*2
        rushPts = math.floor(rush_yd/10) + rush_td*6
        recPts = math.floor(rec_yd/10) + rec_td*6
        miscPts = two_pt_conv*2 - fumbles_lost*2
        
        # If this is a defense, then account for points allowed
        if position == "DEF":
            if pts_allowed == 0:
                d = 10
            elif pts_allowed < 7:
                d = 7
            elif pts_allowed < 14:
                d = 4
            elif pts_allowed < 21:
                d = 1
            elif pts_allowed < 28:
                d = 0
            elif pts_allowed < 35:
                d = -1
            else:
                d = -4
    
        defPts = int_made*2 + fumbles_recovered*2 + sacks + safeties*2 + kick_ret_td*6 + punt_ret_td*6 + d
        totalPts = passPts + rushPts + recPts + miscPts + defPts

    data[date][player]['fantasy_points'] = totalPts
    
    return


def PointsAllowed(text, startPos, endPos, date):
    
    global teams
    global location

    scoreStart = raw_text.find("</td><td>", startPos, endPos) + 9
    scoreEnd = raw_text.find("</td><td>", scoreStart, endPos)
    awayScore = raw_text[scoreStart:scoreEnd]
    
    scoreStart = scoreEnd + 9
    scoreEnd = raw_text.find("</td><td>", scoreStart, endPos)
    homeScore = raw_text[scoreStart:scoreEnd]
    
    for team in teams:
        if team == location:
            data[date][team + " Defense"]['pts_allowed'] = awayScore
        else:
            data[date][team + " Defense"]['pts_allowed'] = homeScore

    return
    

### ========================================================= ###
###                      START CODE                           ### 
### ========================================================= ###

# Go to each box score from 2012 to 2015
for y in range(0, 4):
    week_count = -1
    year = y + 12
    soup.append(BeautifulSoup(urllib2.urlopen('http://www.pro-football-reference.com/years/' + str(2000 + year) + '/games.htm')))
    tags.append(soup[y].findAll(href = re.compile('/boxscores/' + str(2000 + year) + '........\.htm')))
    weeks.append(soup[y].findAll(csk = re.compile('\d')))
    week = 0
    while week < len(weeks[y]):
        if str(weeks[y][week]).find('-') > -1:
            weeks[y].remove(weeks[y][week])
        week += 1
    
    # For each box score, grab the raw HTML to be used to text mine
    for t in tags[y]:
        week_count += 1
        count += 1
        SoupOffensePlayers = list()
        url = 'http://www.pro-football-reference.com' + str(t).split('"')[1]
        raw_text = (urllib2.urlopen(url).read())
        week = str(weeks[y][week_count])
        week = week[week.find("csk") + 8:week.find("</td>")].replace(">", "")

        # Find the game date.  Find the text positions for something that looks like a date,
        # and then return this as the game date.
        for month in months:
            if month in raw_text:
                dateStart = raw_text.find("- " + month + " ") + 2
                dateEnd = raw_text.find(", 2", dateStart, dateStart + 24) + 6
                if raw_text[dateStart:raw_text.find(" ", dateStart, dateEnd)] in months:
                    date = raw_text[dateStart:dateEnd]
                    
        replace_list = list()
        replace_list = ('st', 'nd', 'rd', 'th')
        for j in replace_list:
            date = date.replace(j, '')

        # Proceed only if the game has been played
        if parser.parse(date) < datetime.datetime.today():

            # Initialize the structure of the date dictionary
            data[date] = dict()
        
            # Find the stadium location.  In the raw text, this is right before the date,
            # so we'll use the previously determined date text positions to find the location text positions 
            locationStart = raw_text.find(" at ", dateStart - 50, dateStart) + 5
            locationEnd = raw_text.find(" -", locationStart + 4, dateStart)
            location = locations[raw_text[locationStart:locationEnd]]
        
            # Find text positions for offensive statistics
            offenseStart = raw_text.find("Passing, Rushing, ")
            offenseEnd = raw_text.find("Defense", offenseStart, len(raw_text))
            
            # Append offensive statistics to dictionary
            OffenseStats(raw_text, offenseStart, offenseEnd, date)
    
            # Find text positions for return statistics
            if raw_text.find("Kick/Punt Returns") > -1:
                returnStart = raw_text.find("Kick/Punt Returns")
                returnEnd = raw_text.find("Kicking & Punting")
                # Append return statistics to dictionary
                ReturnStats(raw_text, returnStart, returnEnd, date)
    
            # Create dictionaries for both defenses
            for team in teams:
                defense = str(team) + " Defense"
                data[date][defense] = {'position':'DEF','team':team,'opponent':0,'location':0,'cmp':0,'pass_att':0,'pass_yd':0,'pass_td':0,'int_thrown':0,'pass_long':0,'rush_att':0,'rush_yd':0,'rush_td':0,'rush_long':0,'targets':0,'receptions':0,'rec_yd':0,'rec_td':0,'rec_long':0,'fumbles':0,'fumbles_lost':0,'int_made':0,'int_yds':0,'int_td':0,'int_long':0,'sacks':0.0,'tackles':0,'ast':0,'fumbles_recovered':0,'fum_yds':0,'fum_rec_td':0,'forced_fumbles':0,'safeties':0,'kick_ret':0,'kick_ret_yds':0,'yds_per_kick_ret':0,'kick_ret_td':0,'kick_ret_long':0,'punt_ret':0,'punt_ret_yds':0,'yds_per_punt_ret':0,'punt_ret_td':0,'punt_ret_lng':0,'xpm':0,'xpa':0,'fgm':0,'fga':0,'fg_made_lengths':0,'fg_missed_lengths':0,'off_snap_count':0,'off_snap_count_pct':0,'def_snap_count':0,'def_snap_count_pct':0,'st_snap_count':0,'st_snap_count_pct':0,'fantasy_points':0,'qbr':0,'two_pt_conv':0,'pts_allowed':0,'season':year + 2000,'week':0}
                
            # Find text positions for defense statistics
            defenseStart = raw_text.find("Sacks &amp; Tackles")
            if raw_text.find("Kick/Punt Returns") > -1:
                defenseEnd = raw_text.find("Kick/Punt Returns")
            else:
                defenseEnd = raw_text.find("Kicking & Punting")
            
            # Append defense statistics to dictionary    
            DefenseStats(raw_text, defenseStart, defenseEnd, date)

            # Append successful two point conversion attempts to dictionary
            TwoPtConv(raw_text, date)
    
            # Find text position for kicker statistics
            kickerStart = raw_text.find("Kicking & Punting")
            kickerEnd = raw_text.find("Starting Lineups")
    
            # Find text position for positions
            posStart = raw_text.find("Snap Counts", kickerEnd, len(raw_text))
            posEnd = raw_text.find("Pass Targets", kickerEnd, len(raw_text))
    
            # Append positions and snap count to dictionary
            Positions(raw_text, posStart, posEnd, date)
            
            # Append kicking statistics to dictionary
            KickerStats(raw_text, kickerStart, kickerEnd, date)
    
            # Append opponents to dictionary
            Opponents(date)
    
            # Find text positions for points allowed statistics
            ptsStart = raw_text.find("End of Regulation")
            ptsEnd = raw_text.find("Scoring plays", ptsStart, len(raw_text))
    
            # Append points allowed by each team to dictionary
            PointsAllowed(raw_text, ptsStart, ptsEnd, date)
                            
            # Append additional stats to dictionary
            for players in data[date]:
    
                # Quarterback rating
                completions = float(data[date][players]['cmp'])
                attempts = float(data[date][players]['pass_att'])
                yards = float(data[date][players]['pass_yd'])
                touchdowns = float(data[date][players]['pass_td'])
                interceptions = float(data[date][players]['int_thrown'])
                data[date][players]['qbr'] = Qbr(completions, attempts, yards, touchdowns, interceptions)
    
                # Stadium location
                data[date][players]['location'] = location
                
                # Week number
                data[date][players]['week'] = week
    
                # Fantasy points using standard scoring
                x = list()
                parameters = list()
                parameters = ('position','pass_yd','pass_td','int_thrown','rush_yd','rush_td','rec_yd','rec_td','fumbles_lost','int_made','int_td','sacks','fumbles_recovered','fum_rec_td','safeties','kick_ret_td','punt_ret_td','two_pt_conv','pts_allowed','xpm','xpa','fgm','fga','fg_made_lengths')
                for p in parameters:
                    if (p <> "position") and (p <> "fg_made_lengths"):
                        x.append(int(data[date][players][p]))
                    else:
                        x.append(data[date][players][p])
    
                FantasyPoints(date, players, x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10], x[11], x[12], x[13], x[14], x[15], x[16], x[17], x[18], x[19], x[20], x[21], x[22], x[23])
                
                # Some players are not included in the positions on the box score.  Fix that here.
                if players in otherPlayers:
                    data[date][players]['position'] = otherPlayers[players]
                    
                # If player doesn't have a position for this date but does in a previous box score, include that position
                if data[date][players]['position'] == 0:
                    for dates in data:
                        if (players in data[dates]) and (data[dates][players]['position']) <> 0:
                            data[date][players]['position'] = data[dates][players]['position']
                            break
                            
            # Initialize box score HTML again
            del raw_text
    
            # Append to list that will be written in csv file
            for p in data[date]:
                OutputList = list()
                for h in headings:
                    if h == 'player':
                        OutputList.append(p)
                    elif h == 'date':
                        OutputList.append(date)
                    else:
                        OutputList.append(data[date][p][h])
                OutputData.append(OutputList)

# Write output to CSV file at the end
with open('C:/Users/Matt/Desktop/fantasy_data.csv', "w") as output:
    writer = csv.writer(output, delimiter = ',', lineterminator = '\n')
    writer.writerow(list(headings))
    for line in range(len(OutputData)):
        # Make sure the team name exists.  It won't exist if it is a kicker that did a kickoff but no field goals.  Should not include this person.
        if OutputData[line][2] <> 0:
            writer.writerow(OutputData[line])
