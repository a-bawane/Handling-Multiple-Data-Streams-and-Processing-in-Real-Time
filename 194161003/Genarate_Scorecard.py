import re
#import operator

#filename="194161003-4149-commentary.txt"
#outfile=open("194161003-4149-scorecard-computed.txt","w+")
run_dict = {"1": 1, "2": 2, "3": 3, "4":4,"NO": 0,"5":5,"6":6,"7":7,"FOUR": 4, "SIX": 6, "no": 0, "four": 4, "six": 6}
extras_dict = {"leg bye": 1,"leg byes": 1,"wides": 2, "wide": 2, "no ball": 3, "run": -1,"byes": 0, "bye": 0, "runs": -1}
f1 = open("teams.txt")
lines = f1.readlines()
country_dict = {}
for l in lines:
    matchObj = re.match(r'(.*):(.*).*', l, re.M | re.I)
    if matchObj:
        country_dict[matchObj.group(1)] = matchObj.group(2).split(",")
f1.close()

space_adjust_long=38
space_adjust_mid=7
space_adjust_small=10
class Batsman:

    def __init__(self, name="", dismissal_method="not out", run=0, balls=0, minutes="00", fours=0, sixes=0, strike_rate=0):
        self.name = name
        self.dismissal_method = dismissal_method
        self.run = run
        self.balls = balls
        self.minutes = minutes
        self.fours = fours
        self.sixes = sixes
        self.strike_rate = strike_rate

    def update_batsman(self, run=0, dismissal_method="not out", minutes="00"):
        self.run += run
        self.balls += 1
        self.strike_rate = self.run / self.balls * 100
        self.dismissal_method = dismissal_method
        self.minutes = minutes
        if run == 4 or run == 5:
            self.fours += 1
        if run == 6 or run == 7:
            self.sixes += 1

    def get_name(self):
        return self.name

    def get_method(self):
        return self.dismissal_method

    def print_batsman(self,outfile):
        outfile.write(self.name.ljust(space_adjust_long)+ self.dismissal_method.ljust(space_adjust_long)+ str(self.run).ljust(space_adjust_mid)+str(self.balls).ljust(space_adjust_mid)+\
              str(self.minutes)[:-1].ljust(space_adjust_mid)+str(self.fours).ljust(space_adjust_mid)+ str(self.sixes).ljust(space_adjust_mid)+ str(round(self.strike_rate,2)).ljust(space_adjust_mid)+"\n")


class Bowler:

    def __init__(self, name="", over=0, maiden_over=0, run=0, wickets=0, economy=0, zeros=0, fours=0, sixes=0, wides=0,no_balls=0):
        self.name = name
        self.overs = over
        self.balls = 0
        self.maiden_over = maiden_over
        self.run = run
        self.wickets = wickets
        self.economy = economy
        self.zeros = zeros
        self.fours = fours
        self.sixes = sixes
        self.wides = wides
        self.no_balls = no_balls
        self.run_in_over = 0

    def update_bowler(self, run=0, wickets=0, wides=0, no_balls=0):
        if wides != 1 or no_balls != 1:
            self.run += run
        self.balls += 1
        self.wickets += wickets
        if wides == 1 or no_balls == 1:
            self.wides += wides
            self.no_balls += no_balls
            self.balls -= 1
        if run == 4 or run == 5:
            self.fours += 1
        if run == 6 or run == 7:
            self.sixes += 1
        if run==0 :
            self.zeros+=1
        if self.balls % 6 != 0:
            self.overs += 0.100
        else:
            self.overs = self.balls / 6
        self.run_in_over += run
        if self.balls % 6 == 0:
            if self.run_in_over == 0:
                self.maiden_over += 1
            self.run_in_over = 0
        if self.balls!=0:

            self.economy = self.run / self.balls * 6
    def get_name(self):
        return self.name

    def print_bowler(self,outfile):
        outfile.write(str(self.name.ljust(space_adjust_long))+str(round(self.overs,1)).ljust(space_adjust_mid)+str(int(self.maiden_over)).ljust(space_adjust_small)+ str(self.run).ljust(space_adjust_small)+\
              str(self.wickets).ljust(space_adjust_small)+str(round(self.economy,2)).ljust(space_adjust_small)+str(self.zeros).ljust(space_adjust_small)+str(self.fours).ljust(space_adjust_small)+ \
              str(self.sixes).ljust(space_adjust_small)+ str(self.wides).ljust(space_adjust_small)+str(self.no_balls).ljust(space_adjust_small)+"\n")


class BatsmanScorecard:

    def __init__(self, player_list, name="", number=0):
        self.innings_name = name
        self.innings_number = number
        self.batsman_list = []
        self.overs = 0
        self.balls = 0
        self.run_rate = 0
        self.yet_to_bat = player_list
        self.extras_list = [0, 0, 0, 0]  # (b,lb,nb,wd)
        self.total = 0
        self.fall_of_wickets = []  # [score,name, over]

    def update_batsman_scorecard(self, run=0, extra_index=-1):

        self.total += run
        if extra_index==3:
            self.total+=1
        self.balls += 1
        if extra_index in (2, 3):
            self.balls -= 1
        if extra_index in [0,1,2]:
            self.extras_list[extra_index] += run
        if extra_index ==3:
            self.extras_list[extra_index] +=1
        if self.balls % 6 != 0:
            self.overs += 0.100
        else:
            self.overs = self.balls / 6
        if self.balls!=0:

            self.run_rate = self.total / self.balls * 6

    def update_batsman_list(self, batsman, run=0, extra_index=-1):

        self.update_batsman_scorecard(run, extra_index)
        flag = False
        for i in self.batsman_list:

            if i.get_name().find(batsman) != -1:
                if extra_index in [-1, 3]:
                    i.update_batsman(run)
                elif extra_index in [0, 1]:
                    i.update_batsman()

                flag = True
                break
            else:
                flag = False
        if not flag:
            for i in self.yet_to_bat:

                if i.get_name().find(batsman) != -1:
                    i.update_batsman(run)
                    self.yet_to_bat.remove(i)
                    self.batsman_list.append(i)
                    break


    def update_wicket(self, batsman, method, minutes, run=0, extra_index=-1):
        self.update_batsman_scorecard(run, extra_index)

        for i in self.batsman_list:
            flag1 = False

            if i.get_name().find(batsman) != -1:
                i.update_batsman(run=run, dismissal_method=method, minutes=minutes)
                flag1 = True
                break
            if not flag1:
                for i in self.yet_to_bat:

                    if i.get_name().find(batsman) != -1:

                        self.yet_to_bat.remove(i)
                        self.batsman_list.append(i)
                        i.update_batsman(run=run, dismissal_method=method, minutes=minutes)
                        break
        self.fall_of_wickets.append([self.total, batsman, round(self.overs, 1)])

    def get_yet_to_list(self):
        return self.yet_to_bat


    def get_batsman_list(self):
        return self.batsman_list

    def print_batsman_scorecard(self,outfile):
        if self.innings_number==1:
            outfile.write(self.innings_name+" Innings"+" ("+str(round(self.overs,1))+" overs maximum)"+"\n")
        else:
            outfile.write(self.innings_name+" Innings"+ "("  +str(round(self.overs, 1))+")"+"\n")

        outfile.write("BATSMEN".ljust(space_adjust_long)+"   ".ljust(space_adjust_long)+"R".ljust(space_adjust_mid)+"B".ljust(space_adjust_mid)+\
              "M".ljust(space_adjust_mid)	+	"4s".ljust(space_adjust_mid)	+	"6s".ljust(space_adjust_mid)	+"SR".ljust(space_adjust_mid)+"\n")
        for i in self.batsman_list:
            i.print_batsman(outfile)


        sum = 0
        j=0
        final=""
        temp=["b","lb","w","nb"]
        for i in self.extras_list:
            if self.extras_list[j] !=0:
                final=final+temp[j]+" "+str(self.extras_list[j])+", "

            j+=1
            sum += i
        outfile.write("Extras".ljust(space_adjust_mid*11)+ str(sum)+" ("+str(final)[:-2]+")"+"\n")
        wick=0
        for i in self.batsman_list:
            if i.get_method()!="not out":
                wick+=1
        if wick==10:
            wick=" all out "
        else:
            wick="/"+str(wick)

        outfile.write("TOTAL".ljust(space_adjust_mid*11)+str(self.total)+str(wick)+ " ("+str(round(self.overs,1))+ " Overs, "+"RR: "+str(round(self.run_rate,2))+")"+"\n")
        oout_str1=""
        if len(self.yet_to_bat)!=0:

            oout_str1+="Did not bat: "
            for i in self.yet_to_bat:
                oout_str1+=str(i.get_name())+", "

            outfile.write(oout_str1[:-2]+"\n")
        j = 0
        if len(self.fall_of_wickets)!=0:
            final_output="Fall of wickets: "
            for val in self.fall_of_wickets:
                for i in self.batsman_list:

                    if i.get_name().find(val[1]) != -1:

                        j+=1
                        final_output+=(str(j)+"-"+str(val[0])+" ("+str(i.get_name())+", "+str(val[2])+" ov)"+", ")
                        break
            outfile.write(final_output[:-2]+"\n")


class BowlerScorecard:

    def __init__(self, player_list, name=0, number=0):
        self.innings_name = name
        self.innings_number = number
        self.bowler_list =[]
        self.temp_player_list=player_list
    def update_bowler_scorecard(self, bowler,run=0,extras=-1,wicket=0):

        wide = 0
        j=0
        no_balls = 0
        if extras==2:
            wide=1
        if extras==3:
            no_balls=1
        if extras in [0,1]:
            run=0

        flag = False
        for i in self.bowler_list:

            if i.get_name().find(bowler) != -1:
                i.update_bowler(run=run, wickets=wicket, wides=wide, no_balls=no_balls)

                flag = True
                break
            else:
                flag = False

        if not flag:
            for i in self.temp_player_list:
                # #print("here")
                if i.get_name().find(bowler) != -1:
                    i.update_bowler(run=run, wickets=wicket, wides=wide, no_balls=no_balls)
                    self.temp_player_list.remove(i)
                    self.bowler_list.append(i)
                    break


    def print_bowler_scorecard(self,outfile):

        outfile.write("Bowling".ljust(space_adjust_long)+"O".ljust(space_adjust_mid)+"M".ljust(space_adjust_small)	+"R".ljust(space_adjust_small)+"W".ljust(space_adjust_small)+\
              "Econ".ljust(space_adjust_small)+	"0s".ljust(space_adjust_small)+"4s".ljust(space_adjust_small)+"6s".ljust(space_adjust_small)+"WD".ljust(space_adjust_small)+"NB".ljust(space_adjust_small)+"\n")
        for i in self.bowler_list:
            i.print_bowler(outfile)




class match(Batsman,BatsmanScorecard,Bowler,BowlerScorecard):

    def __init__(self,outfile):
        self.first_team=None
        self.second_team=None
        self.first_inning_batsman_card = None
        self.second_inning_bowler_card = None
        self.second_inning_batsman_card = None
        self.first_inning_bowler_card = None
        self.match_vs={}
        self.wickets_list=[]
        self.outfile=outfile
        self.flag=0
        self.flag2 = 0
        self.inning_bat=None
        self.inning_ball=None
        self.flag3=0
    def redirect(self,line):
        line = line.split("___")[-1]

        if not self.flag2:
            matchObj = re.match(r'(.*):(.*).*', line, re.M | re.I)

            if matchObj and matchObj.group(1) in country_dict:
                self.match_vs[matchObj.group(1)] = matchObj.group(2).split(",")
                if not self.flag:
                    self.first_team = matchObj.group(1)
                else:
                    self.second_team = matchObj.group(1)
                self.flag += 1

            if self.flag>=2:
                for k, v in self.match_vs.items():
                    i = 0
                    for j in v:
                        name = re.sub(r'\d', "", j)
                        self.match_vs[k][i] = name.strip()
                        i += 1
                self.intialize_match()
                self.flag2=1

        else:
            self.process_commentary_line(line)


    def intialize_match(self):
        temp_batsman_list = []
        temp_bowler_list = []
        for i in self.match_vs[self.first_team]:
            player_batsman = Batsman(name=i)
            temp_batsman_list.append(player_batsman)
            player_bowler = Bowler(name=i)
            temp_bowler_list.append(player_bowler)
        self.first_inning_batsman_card = BatsmanScorecard(name=self.first_team, number=1, player_list=temp_batsman_list)
        self.second_inning_bowler_card = BowlerScorecard(name=self.first_team, number=2, player_list=temp_bowler_list)
        temp_batsman_list = []
        temp_bowler_list = []
        for i in self.match_vs[self.second_team]:
            player_batsman = Batsman(name=i)
            temp_batsman_list.append(player_batsman)
            player_bowler = Bowler(name=i)
            temp_bowler_list.append(player_bowler)
        self.second_inning_batsman_card = BatsmanScorecard(name=self.second_team, number=2, player_list=temp_batsman_list)
        self.first_inning_bowler_card = BowlerScorecard(name=self.second_team, number=1, player_list=temp_bowler_list)
        self.inning_bat = self.first_inning_batsman_card
        self.inning_ball= self.first_inning_bowler_card
        self.wicket_list = []

    def process_commentary_line(self,line):

            #line=line.split("___")[-1]

            if line.strip() == "##########":
                self.inning_bat = self.second_inning_batsman_card
                self.inning_ball = self.second_inning_bowler_card
                self.wicket_list=[]
                self.flag3=1


            matchObj2 = re.match(r"(.*?)\d(.*?)SR:.*", line[0:100], re.M | re.I)
            if matchObj2:
                temp_var = re.sub(r'^\d', "", matchObj2.group(2).strip())

                self.wicket_list.append([matchObj2.group(1).strip(), temp_var.split("(")[1].split()[0]])
            matchObj = re.match(r'(.*?) to (.*?),(.*?)(run|runs|leg bye|leg byes|wide|wides|bye|byes|no ball|OUT),(.*)', line[0:100],re.M | re.I)

            if matchObj:
                temp_list = (matchObj.group().strip()).split(",")


                minutes=0
                if temp_list[1].split()[0].strip() == "OUT":

                    for i in self.wicket_list:
                        if i[0].find(matchObj.group(2).strip()) != -1:

                            method = i[0].split(matchObj.group(2).strip())[1].strip()

                            if i[-1]==" ":
                                minutes=0
                            else:
                                minutes = i[-1]

                            run=matchObj.group(5).split("run")[0].strip()
                            if run.isdigit() :
                                run=int(run)
                            else:
                                run=0
                            self.inning_bat.update_wicket(matchObj.group(2).strip(), method, minutes,run=run)

                            break
                    self.inning_ball.update_bowler_scorecard(matchObj.group(1).strip(),wicket=1)
                    return
                e_index = -1
                for k, v in extras_dict.items():
                    if temp_list[1].find(k) != -1:
                        e_index = v
                        break

                if e_index==3:
                    runs=run_dict[temp_list[1].split(")")[1].strip().split()[0]]
                else:
                    runs=run_dict[temp_list[1].split()[0]]

                self.inning_ball.update_bowler_scorecard(matchObj.group(1).strip(),runs,e_index)
                self.inning_bat.update_batsman_list(matchObj.group(2).strip(), runs, e_index)
            self.write_scorecard()

    def write_scorecard(self):
        outfile=open(self.outfile,'w+')
        self.first_inning_batsman_card.print_batsman_scorecard(outfile)
        self.first_inning_bowler_card.print_bowler_scorecard(outfile)

        if self.flag3:
            outfile.write("\n")
            self.second_inning_batsman_card.print_batsman_scorecard(outfile)
            self.second_inning_bowler_card.print_bowler_scorecard(outfile)
        outfile.close()