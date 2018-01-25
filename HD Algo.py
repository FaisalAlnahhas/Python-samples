hranks = open("hranks.txt", 'r')
hlines = hranks.readlines()

sranks = open("sranks.txt", 'r')
slines = sranks.readlines()

hospitals = {}
students = {}
matches = {}
free_h = []
free_s = []

matching =""

total_av_pos = 21

class Hospitals:
    def __init__(self, data):
        self.av_pos = int(data.split(',')[1])
        self.order_pref = data.strip('\n').split(',')[2:]
        self.ind = 0

class Students:
    def __init__(self, data):
        self.order_pref = data.strip('\n').split(',')[2:]
        self.matched = False

# grab attributes of Students class and store them
for i in range(len(slines)):
    students[slines[i].split(",")[0]] = Students(slines[i])

# same for hospitals
for i in range(len(hlines)):
    hospitals[hlines[i].split(",")[0]] = Hospitals(hlines[i])

#initialize names as keys and empty lists as values
for keys, vals in hospitals.items():
    matches[keys] = []

# add free hospitals to free_h, and do same for students
for keys in hospitals:
    free_h.append(keys)

for keys in students:
    free_s.append(keys)

# begin while loop based on available positions (21)
while total_av_pos != 0:
    hs = free_h[len(free_h)-1]
    #look at key's pre list's index
    ds = hospitals[hs].order_pref[hospitals[hs].ind]
    # go up in the list
    hospitals[hs].ind += 1

    if students[ds].matched == False:
        #if d and h haven't been matched yet, add ds to hs list
        # which is value of dictionary matches
        matches[hs].append(ds)
        # decrement available positions once a pos is assigned
        open_pos = Hospitals[hs].av_pos
        open_pos -= 1
        if open_pos == 0:
            # remove hospital from list of free_h
            free_h.remove(hs)
        # a match happened
        students[ds].matched = True
        total_av_pos -= 1
        #compare index of d's pref with h's pref, if d's higher unmatch existing
        #match and make a new match
    
        current_index = students[ds].order_pref.index(students[ds].order_pref)                                           
    elif (students[ds].order_pref.index > current_index):
        #unmatch
        matches[students[ds].matching].remove(ds)
        if hospitals[students[ds].matching].av_pos < 1:
            # add new hospital to free_h
            free_h.append(students[ds].matching)
        #account for new open positions
        hospitals[students[ds].matching].av_pos += 1
        #add new hospital to matched hospitals
        matches[hs].append(ds)
        #decrement open pos in hosptials
        hospitals[hs].av_pos -= 1
        if hospitals[hs].av_pos == 0:
            hospitals[hs].remove(hs)

fout = open("matches.txt", 'w')
fout.write(matches())
fout.close()

                                                
    


