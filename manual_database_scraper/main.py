import pandas as pd
import winsound

def extract(raw,find,after = True,qms=False):
    loc = raw.find(find)
    if loc == -1:
        return ""
    if after:
        loc += len(find)
    substr = raw[loc:]
    if qms:
        return substr[:substr.find("\"")].strip()
    else:
        return substr[:min(substr.find(">"),substr.find("<"))].strip()
    

def extract_imgs(raw,find):
    v = False
    if v:
        print("\nExtracting",find,"at",raw.find(find),"\n")
    loc = raw.find(find)
    if loc == -1:
        return [""]
    
    substr = raw[loc+len(find):]
    loc = substr.find("Characters (event):")
    if loc == -1:
        loc = substr.find("Supports (hint):")
        if loc == -1:
            loc = substr.find("Supports (event):")
            if loc == -1:
                loc = substr.find("Rarity:")
    
    substr = substr[:loc]
    substrs = substr.split('<img src="')
    if v:
        print(substrs)
    arr = []
    for i in substrs:
        name = extract(i,"alt=\"",after = True, qms = True)
        img = "https://gametora.com/images/umamusume/"+extract(i,"/images/umamusume/",after = True, qms = True)
        if name != "":
            arr.append([name,img])
    if v:
        print("\nGot",arr)
    return arr


def extract_other_vers(raw,title):
    v = False
    if v:
        print("\nExtracting",title,"\n")
    
    if raw.find(title) == -1:
        return ""
    substr = raw[raw.find(title)+len(title):]
    #index = substr.find("Supports (hint):")
    #if index == -1:
    #    index = substr.find("Supports (event):")
    #    if index == -1:
    index = substr.find("Activation:")
    
    substr = substr[:index]
    
    
    max_loops = 100
    loop = 0
    if substr.find("<") > substr.find("<"):
        print("WARNING: SUBSTR STARTS AT THE WRONG POINT?")
        print(substr)
        return ""
        
    while substr.find("<") != -1 and substr.find("<") <= len(substr): # idk what bug is causing that second condition to be nessesary
        substr = substr[:substr.find("<")] + "|" + substr[substr.find(">")+1:]
        if v:
            print(substr)
            print(substr.find("<"))
        loop += 1
        if loop > max_loops or len(substr) > 5000:
            if loop > max_loops:
                print("ERROR: EXCEEDED MAX LOOPS")
            else:
                print("ERROR: INPUT STRING TOO LONG:",len(substr))
                
            print(substr)
            print(substr.find("<"))
            return ""
    while substr.find("||") != -1:
        substr = substr.replace("||","|")
    out = []
    for i in substr.split("|"):
        if i != "":
            out.append(i)
    return out

all = {}
all["ID"] = []
all["ICO"] = []
all["NAME"] = []
all["DESC_INGAME"] = []
all["DESC_DETAILED"] = []
all["CHARACTERS"] = []
all["CHARACTERS_EVENT"] = []
all["RARITY"] = []
all["SIBLINGS"] = []
all["HINT_SOURCES"] = []
all["EVENT_SOURCES"] = []
all["ACTIVATION"] = []
all["BASE_COST"] = []
all["CONDITIONS"] = []
all["COND_LINK"] = []
all["DURATION"] = []
all["EFFECT1"] = []
all["EFFECT2"] = []
all["EFFECT3"] = []

iters = 0

all_errors = []
last_read_name = "start"
    
raw = "------------------------------"
while len(raw) > 12 or len(raw) < 3:
    # todo test @
    raw = input(">").replace("<b>","").replace("</b>","").replace("<div style=\"white-space: pre-wrap;\">","")
    
    if len(raw) < 3:
        continue
    if len(raw) < 12:
        break
    
    #img = raw[raw.find("<img src="):raw.find(".png"eerrrrrrr)+6]
    #name = raw[raw.find("<span><div>"):raw.find("</div></span>")]
    #print(raw)
    name = extract(raw, "<span><div>",after=True)
    if name == "":
        print("ERROR: BAD READ. CONTINUING")
        all_errors.append(["BAD READ",last_read_name,raw])
        winsound.Beep(940, 500) 
        continue
    if name == last_read_name:
        print("ERROR: Duplicate entry.")
        all_errors.append(["Duplicate",last_read_name,raw])
        winsound.Beep(940, 500) 
        continue
    all["NAME"].append(name)
    all["ID"].append(iters)
    
    all["ICO"].append("https://gametora.com"+extract(raw, "<img src=\"",after=True,qms=True))
    
    #desc1 = raw[raw.find("Description (in-game)"):raw.find("Description (detailed)")]
    all["DESC_INGAME"].append(extract(raw, "Description (in-game):"))
    #desc2 = raw[raw.find("Description (detailed)"):raw.find("Rarity:")]
    all["DESC_DETAILED"].append(extract(raw, "Description (detailed):"))
    
    all["CHARACTERS"].append(extract_imgs(raw, "Characters:"))
    
    all["CHARACTERS_EVENT"].append(extract_imgs(raw, "Characters (event):"))
    
    all["RARITY"].append(extract(raw, "Rarity:"))
    # TODO OTHER VERSIONS
    #others = raw[raw.find("Other versions:"):raw.find("</span></span>")]
    #conditions = raw[raw.find("Conditions:"):raw.find("</div></div><div>")]
    sibs = extract_other_vers(raw,"Other versions:")
    all["SIBLINGS"].append(sibs)
    hints = extract_imgs(raw,"Supports (hint):")
    all["HINT_SOURCES"].append(hints)
    events = extract_imgs(raw,"Supports (event):")
    all["EVENT_SOURCES"].append(events)
    

    
    all["ACTIVATION"].append(extract(raw, "Activation:"))
    all["BASE_COST"].append(extract(raw, "Base cost:"))
    
    
    all["CONDITIONS"].append(extract(raw, "Conditions:").replace("&gt;"," >").replace("&lt;"," <").replace("&amp;","\n&").replace("@","\n@\n").replace("  "," "))
    #cond_link = raw[raw.find("/umamusume/skill-condition-viewer?skill="):raw.find(">Show conditions in the viewer")]
    all["COND_LINK"].append("https://gametora.com"+extract(raw, "/umamusume/skill-condition-viewer?skill=",qms=True,after=False))
    #dur = raw[raw.find("Base duration:"):raw.find("</div></div><div>")]
    all["DURATION"].append(extract(raw, "Base duration:"))
    # merge following two
    eff1 = extract(raw, "Effect:")
    
    if eff1 == "":
        eff1 = extract(raw, "Effect 1:")
    else:
        if extract(raw, "Effect 1:") != "":
            print("ERROR WEIRD EFF NAME PATTERN")
            print(eff1)
            print(extract(raw, "Effect 1:"))
            all_errors.append(["Weird eff pattern",last_read_name,raw])
            #continue
            
    all["EFFECT1"].append(eff1)
    all["EFFECT2"].append(extract(raw, "Effect 2:"))
    all["EFFECT3"].append(extract(raw, "Effect 3:"))
    
    
    if sibs == "" and raw.find("Other versions:") != -1:
        print("ERROR: Sibs process failed for some reason")
        all_errors.append(["Sibs failure",last_read_name,raw])
        winsound.Beep(940, 500) 
        continue
    if hints == "" and raw.find("Supports (hint):") != -1:
        print("ERROR: Hints process failed for some reason")
        all_errors.append(["Hints failure",last_read_name,raw])
        winsound.Beep(940, 500) 
        continue
    if events == "" and raw.find("Supports (event):") != -1:
        print("ERROR: Events process failed for some reason")
        all_errors.append(["Events failure",last_read_name,raw])
        winsound.Beep(940, 500) 
        continue
    
    if eff1 == "":
        print("ERROR: Skill with no effect is being processed.")
        all_errors.append(["No effect",last_read_name,raw])
        winsound.Beep(940, 500) 
        continue
    
    last_read_name = name
    
    print("\nSuccess reading",name,"\n")
    winsound.Beep(440, 500) 
    
    iters += 1
    if iters % 10 == 0:
        try:
            df = pd.DataFrame(all)
            df.to_csv('output.csv', index=False)
            df = None
        except:
            print("CATASTROPHIC ERROR, FAILED TO BUILD DF")
            print(all)
            winsound.Beep(940, 500) 
            
try:
    # Write the DataFrame to a CSV file
    df = pd.DataFrame(all)
    df.to_csv('output.csv', index=False)
    print("Written")
except:
    print("CATASTROPHIC ERROR, FAILED TO BUILD DF")
    print(all)
    
    
winsound.Beep(340, 100) 
print("Printing all errors:")
for i in all_errors:
    print(i)

# issue with <div class="tooltips_tooltip__NxFYo"><div class="skills_skill_tooltip__JIWMZ"><div class="tooltips_tooltip_line__OStyx utils_padbottom__C1WA5"><div style="padding: 5px;" class="sc-1b03763b-0 dnlGQR"><div><div class="sc-9ae1b094-0 fVBhhN"><span style="max-width: 50px; max-height: 50px; display: inline-block; margin-top: auto; margin-bottom: auto; filter: var(--image-dim);"><img src="/images/umamusume/skill_icons/utx_ico_skill_20041.png" style="max-width: 100%; height: auto; display: flex;" loading="lazy" alt=""></span><div class="sc-9ae1b094-1 hwTozI"><span><div>Straight Descent</div></span></div></div></div></div></div><div class="tooltips_tooltip_line__OStyx"><b>Description (in-game):</b> Slightly improve running on a downhill. (Pace Chaser)</div><div class="tooltips_tooltip_line__OStyx"><b>Description (detailed):</b> <span style="text-decoration: underline dotted; cursor: help;" aria-expanded="false">Unknown</span></div><div class="tooltips_tooltip_line__OStyx"><div><b>Characters:</b></div><span class="tooltips_inline_image__Zi70Y" aria-expanded="false"><span class="dimmed undefined" style="max-width: 50px; max-height: 50px; display: inline-block; filter: var(--image-dim);"><img src="/images/umamusume/characters/thumb/chara_stand_1030_103001.png" style="max-width: 100%; height: auto;" loading="lazy" alt="Rice Shower"></span></span></div><div class="tooltips_tooltip_line__OStyx"><div><b>Supports (hint):</b></div><span class="tooltips_inline_image__Zi70Y" aria-expanded="false"><span class="dimmed undefined" style="max-width: 50px; max-height: 50px; display: inline-block; filter: var(--image-dim);"><img src="/images/umamusume/supports/support_card_s_30023.png" style="max-width: 100%; height: auto;" loading="lazy" alt="Rice Shower"></span></span><span class="tooltips_inline_image__Zi70Y" aria-expanded="false"><span class="dimmed undefined" style="max-width: 50px; max-height: 50px; display: inline-block; filter: var(--image-dim);"><img src="/images/umamusume/supports/support_card_s_10015.png" style="max-width: 100%; height: auto;" loading="lazy" alt="Rice Shower"></span></span></div><div class="tooltips_tooltip_line__OStyx"><div><b>Supports (event):</b></div><span class="tooltips_inline_image__Zi70Y" aria-expanded="false"><span class="dimmed undefined" style="max-width: 50px; max-height: 50px; display: inline-block; filter: var(--image-dim);"><img src="/images/umamusume/supports/support_card_s_20024.png" style="max-width: 100%; height: auto;" loading="lazy" alt="Daitaku Helios"></span></span></div><div class="tooltips_tooltip_line__OStyx"><div><b>Training events:</b></div><span class="tooltips_inline_image__Zi70Y" aria-expanded="false"><span class="dimmed undefined" style="max-width: 50px; max-height: 50px; display: inline-block; filter: var(--image-dim);"><img src="/images/umamusume/scenarios/bnr_ico_008.png" style="max-width: 100%; height: auto;" loading="lazy" alt="Great Food Festival"></span></span></div><div class="tooltips_tooltip_line__OStyx"><b>Rarity:</b> Normal</div><div class="tooltips_tooltip_line__OStyx"><b>Other versions:</b></div><div style="text-align: left;"><div><span class="utils_linkcolor__rvv3k"><span class="utils_linkcolor__rvv3k" aria-expanded="false">Determined Descent</span></span></div></div><div class="tooltips_tooltip_line__OStyx"><b>Activation:</b> Wit check</div><div class="tooltips_tooltip_line__OStyx"><b>Base cost:</b> 120</div><div><div class="tooltips_tooltip_line__OStyx"><b>Conditions:</b><div style="white-space: pre-wrap;">running_style==2&amp;slope==2</div></div><div><div class="tooltips_tooltip_line__OStyx"><a href="/umamusume/skill-condition-viewer?skill=201342">Show conditions in the viewer</a></div></div><div class="tooltips_tooltip_line__OStyx"><b>Base duration:</b> 3 s</div><div><div class="tooltips_tooltip_line__OStyx"><b>Effect:</b> Increase Acceleration (0.2)</div></div></div></div></div>
