import time
import keyboard
import random

# Variables needed for activating some abilities and keeping track of the cooldown

dualcast = False
recastTime = 2.5

verfireReady = False
verfireDuration = 30
verfireStartTime = time.time()

verstoneReady = False
verstoneDuration = 30
verstoneStartTime = time.time()

flecheCooldown = 25
flecheStartTime = time.time()
contreSixteCooldown = 35
contreSixteStartTime = time.time()

corpsCooldown = 35
corpsStartTime = time.time()
corpsStacks = 2
displacementEngagementCooldown = 35
displacementEngagementStartTime = time.time()
displacementEngagementStacks = 2

accelerationActive = False
accelerationCooldown = 55
accelerationStartTime = time.time()
accelerationStacks = 2
swiftcastActive = False
swiftcastCooldown = 60
swiftcastStartTime = time.time()

# Variables for things revolving around the Red Mage Melee Combo

whiteMana = 0
blackMana = 0
manaStacks = 0
scorchActive = False
resolutionActive = False

# Inputs for each Ability

jolt2Input = "1"
impactInput = "alt+1"
veraero3Input = "2"
veraero2Input = "alt+2"
verthunder3Input = "3"
verthunder2Input = "alt+2"
verstoneInput = "4"
verfireInput = "alt+4"
flecheInput = "5"
contreSixteInput = "alt+5"
corpsInput = "q"
engagementInput = "e"
displacementInput = "ctrl+e"
swiftcastInput = "r"
accelerationInput = "alt+r"
riposteInput = "f"
zwerchhauInput = "g"
redoublementInput= "h"

# Functions for Activating Abilities and adding Mana

def addBlackMana(mana):
    global blackMana
    blackMana = blackMana + mana

def addWhiteMana(mana):
    global whiteMana
    whiteMana = whiteMana + mana

def addBothMana(mana):
    global whiteMana, blackMana
    blackMana = blackMana + mana
    whiteMana = whiteMana + mana

def activateVerstone():
    global verstoneReady, verstoneStartTime, verstoneDuration
    verstoneReady = True
    verstoneDuration = 0
    verstoneStartTime = time.time()
    print("Verstone is active!")

def activateVerfire():
    global verfireReady, verfireStartTime, verfireDuration
    verfireReady = True
    verfireDuration = 0
    verfireStartTime = time.time()
    print("Verfire is active!")

def addManaStack():
    global manaStacks
    if manaStacks < 3:
        manaStacks = manaStacks + 1

def useManaStack():
    global manaStacks
    manaStacks = 0

def activateScorch():
    global scorchActive
    scorchActive = True

def deactivateScorch():
    global scorchActive
    scorchActive = False

def activateResolution():
    global resolutionActive
    resolutionActive = True


def deactivateResolution():
    global resolutionActive
    resolutionActive = False

# Instant Cast Modifier Abilities

def flipDualcast():
    global dualcast
    if dualcast == False:
        dualcast = True
    else:
        dualcast = False

def acceleration():
    global accelerationCooldown, accelerationStartTime, accelerationStacks, accelerationActive
    accelerationStackUpdate()
    if keyboard.is_pressed(accelerationInput):
        if accelerationStacks > 0:
            print("Acceleration Active")
            accelerationActive = True
            accelerationStacks = accelerationStacks - 1
            accelerationCooldown = 0
            if accelerationStacks == 1:
                accelerationStartTime = time.time()
        else:
            print("Acceleration cooldown: ", int(55 - accelerationCooldown))
        updates()
        print()

def swiftcast():
    global swiftcastStartTime, swiftcastCooldown, swiftcastActive
    current_time = time.time()
    if keyboard.is_pressed(swiftcastInput):
        if swiftcastCooldown >= 60:
            print("Swiftcast Active!")
            swiftcastActive = True
            swiftcastStartTime = time.time()
            swiftcastCooldown = 0
        else:
            swiftcastCooldown = current_time - flecheStartTime
            print("Swiftcast cooldown: ", int(60 - swiftcastCooldown))
        print()

def swiftcastUpdatePrint():
    global swiftcastCooldown, swiftcastStartTime
    current_time = time.time()
    if swiftcastCooldown >= 60:
        print("Swiftcast available!")
    else:
        swiftcastCooldown = current_time - swiftcastStartTime
        print("Swiftcast cooldown: ", int(60 - swiftcastCooldown))

def flipSwiftcast():
    global swiftcastActive
    swiftcastActive = False

def accelerationStackUpdate():
    global accelerationCooldown, accelerationStartTime, accelerationStacks
    current_time = time.time()
    if accelerationStacks < 2 and accelerationCooldown >= 55:
        accelerationStacks = accelerationStacks + 1
        accelerationStartTime = time.time()
    if accelerationStacks < 2 and accelerationCooldown <= 55:
        accelerationCooldown = current_time - accelerationStartTime

def accelerationStackUpdatePrint():
    global accelerationCooldown, accelerationStartTime, accelerationStacks
    current_time = time.time()
    if accelerationStacks < 2 and accelerationCooldown >= 55:
        accelerationStacks = accelerationStacks + 1
        accelerationStartTime = time.time()
        print("Acceleration is at ", accelerationStacks, " stacks")
    if accelerationStacks < 2 and accelerationCooldown <= 55:
        accelerationCooldown = current_time - accelerationStartTime
        print("Accleration cooldown: ", int(55 - accelerationCooldown))
    else:
        print("Acceleration is at ", accelerationStacks, " stacks")

def flipAcceleration():
    global accelerationActive
    accelerationActive = False

# Recast functions

def recastWait():
    global recastTime
    recastInt = int(recastTime * 2)
    for timer in range(recastInt, 0, -1):
        print("Waiting for recast time:  ", timer/2)
        weaves()
        time.sleep(.5)

def enchantedRecastWait():
    recastInt = int(1.5 * 2)
    for timer in range(recastInt, 0, -1):
        print("Waiting for recast time:  ", timer/2)
        weaves()
        time.sleep(.5)

# 2 Standard Abilities that generate Black and White mana

def jolt2():
    if scorchActive:
        addBothMana(4)
        print("Scorch Hit!")
        deactivateScorch()
        activateResolution()
    elif resolutionActive:
        addBothMana(4)
        print("Resolution Hit!")
        deactivateResolution()
    else:
        if dualcast:
            print("Jolt 2 dualcasted!")
            flipDualcast()
            recastWait()
        elif swiftcastActive:
            print("Jolt 2 Swiftcasted!")
            flipSwiftcast()
            recastWait()
        else:
            for timer in range(2, 0, -1):
                weaves()
                print("Casting Jolt 2 in: ", timer)
                time.sleep(1)
            flipDualcast()
            print("Hit Jolt 2!")
            addBothMana(2)
    print()
    updates()

def impact():
    if dualcast:
        print("Impact dualcasted!")
        flipDualcast()
        recastWait()
    elif swiftcastActive:
        print("Impact Swiftcasted!")
        flipSwiftcast()
        recastWait()
    else:
        for timer in range(5, 0, -1):
            fleche()
            print("Casting Impact in: ", timer)
            time.sleep(1)
            flipDualcast()
    print("Hit Impact!")
    addBothMana(3)
    print()

# Main Abilities that gain Black and White mana

def veraero3():
    if manaStacks == 3:
        verholy()
    else:
        if accelerationActive:
            print("Veraero 3 accelerated!")
            recastWait()
        elif dualcast:
            print("Veraero 3 dualcasted!")
            flipDualcast()
            recastWait()
        elif swiftcastActive:
            print("Veraero 3 Swiftcasted!")
            flipSwiftcast()
            recastWait()
        else:
            for timer in range(5, 0, -1):
                print("Casting Veraero 3 in: ", timer)
                time.sleep(1)
        if accelerationActive:
            activateVerstone()
            flipAcceleration()
        elif random.randint(1, 2) == 2:
            activateVerstone()
        print("Hit Veraero 3!")
        addWhiteMana(6)
    print()

def veraero2():
    if dualcast:
        print("Veraero 2 dualcasted!")
        flipDualcast()
        recastWait()
    elif swiftcastActive:
        print("Veraero 2 Swiftcasted!")
        flipSwiftcast()
        recastWait()
    else:
        for timer in range(2, 0, -1):
            print("Casting Veraero 2 in: ", timer)
            time.sleep(1)
    print("Hit Veraero 2!")
    addWhiteMana(7)
    print()

def verholy():
    if whiteMana < blackMana:
        activateVerstone()
    elif random.randint(1, 4) == 4:
        activateVerstone()
    useManaStack()
    print("Hit Verholy!")
    addWhiteMana(11)
    recastWait()
    activateScorch()


def verthunder3():
    if manaStacks == 3:
        verflare()
    else:
        if accelerationActive:
            print("Verthunder 3 accelerated!")
            recastWait()
        elif dualcast:
            print("Verthunder 3 dualcasted!")
            flipDualcast()
            recastWait()
        elif swiftcastActive:
            print("Verthunder 3 Swiftcasted!")
            flipSwiftcast()
            recastWait()
        else:
            for timer in range(5, 0, -1):
                print("Casting Verthunder 3 in: ", timer)
                time.sleep(1)
        if accelerationActive:
            activateVerfire()
            flipAcceleration()
        elif random.randint(1, 2) == 2:
            activateVerfire()
        print("Hit Verthunder 3!")
        addBlackMana(6)
    print()

def verthunder2():
    if dualcast:
        print("Verthunder 2 dualcasted!")
        flipDualcast()
        recastWait()
    elif swiftcastActive:
        print("Verthunder 2 Swiftcasted!")
        flipSwiftcast()
        recastWait()
    else:
        for timer in range(2, 0, -1):
            print("Casting Verthunder 2 in: ", timer)
            time.sleep(1)
    print("Hit Verthunder 2!")
    addBlackMana(7)
    print()

def verflare():
    if blackMana < whiteMana:
        activateVerfire()
    elif random.randint(1, 4) == 4:
        activateVerfire()
    useManaStack()
    print("Hit Verflare!")
    addBlackMana(11)
    recastWait()
    activateScorch()

def verfire():
    global verfireReady, verfireDuration
    verfireDuration = time.time() - verfireStartTime
    if verfireReady and verfireDuration < 30:
        if dualcast:
            print("Verfire dualcasted!")
            flipDualcast()
            recastWait()
        elif swiftcastActive:
            print("Verfire Swiftcasted!")
            flipSwiftcast()
            recastWait()
        else:
            for timer in range(2, 0, -1):
                print("Casting Verfire in: ", timer)
                time.sleep(1)
        verfireReady = False
        verfireDuration = 30
        print("Hit Verfire!")
        addBlackMana(5)
    else:
        print("Verfire not active!")
        verfireReady = False
        verfireDuration = 30
    print()

def verstone():
    global verstoneReady, verstoneDuration
    verstoneDuration = time.time() - verstoneStartTime
    if verstoneReady and verstoneDuration < 30:
        if dualcast:
            print("Verfire dualcasted!")
            flipDualcast()
            recastWait()
        elif swiftcastActive:
            print("Verstone Swiftcasted!")
            flipSwiftcast()
            recastWait()
        else:
            for timer in range(2, 0, -1):
                print("Casting Verstone in: ", timer)
                time.sleep(1)
        verstoneReady = False
        verstoneDuration = 30
        print("Hit Verstone!")
        addWhiteMana(5)
    else:
        print("Verstone not active!")
        verstoneReady = False
        verstoneDuration = 30
    print()

# Off Global Coooldown Abilities

def fleche():
    global flecheStartTime, flecheCooldown
    current_time = time.time()
    if keyboard.is_pressed(flecheInput):
        if flecheCooldown >= 25:
            print("Hit Fleche!")
            flecheStartTime = time.time()
            flecheCooldown = 0
        else:
            flecheCooldown = current_time - flecheStartTime
            print("Fleche cooldown: ", int(25 - flecheCooldown))
        print()

def flecheUpdatePrint():
    global flecheStartTime, flecheCooldown
    current_time = time.time()
    if flecheCooldown >= 25:
        print("Fleche available!")
    else:
        flecheCooldown = current_time - flecheStartTime
        print("Fleche cooldown: ", int(25 - flecheCooldown))

def contreSixte():
    global contreSixteCooldown, contreSixteStartTime
    current_time = time.time()
    if keyboard.is_pressed(contreSixteInput):
        if contreSixteCooldown >= 35:
            print("Hit Contre Sixte!")
        else:
            contreSixteCooldown = current_time - contreSixteStartTime
            print("Contre Sixte cooldown: ", int(35 - contreSixteCooldown))
        print()

def contreSixteUpdatePrint():
    global contreSixteCooldown, contreSixteStartTime
    current_time = time.time()
    if contreSixteCooldown >= 35:
        print("Contre Sixte available!")
    else:
        contreSixteCooldown = current_time - contreSixteStartTime
        print("Contre Sixte cooldown: ", int(35 - contreSixteCooldown))

def corps():
    global corpsCooldown, corpsStartTime, corpsStacks
    corpsStackUpdate()
    if keyboard.is_pressed(corpsInput):
        if corpsStacks > 0:
            print("Hit Corps-a-corps")
            corpsStacks = corpsStacks - 1
            corpsCooldown = 0
            if corpsStacks == 1:
                corpsStartTime = time.time()
        else:
            print("Corps-a-corps available in: ", int(35 - corpsCooldown))
        print()
        corpsStackUpdate()

def corpsStackUpdate():
    global corpsCooldown, corpsStartTime, corpsStacks
    current_time = time.time()
    if corpsStacks < 2 and corpsCooldown >= 35:
        corpsStacks = corpsStacks + 1
        corpsStartTime = time.time()
    if corpsStacks < 2 and corpsCooldown <= 35:
        corpsCooldown = current_time - corpsStartTime

def corpsStackUpdatePrint():
    global corpsCooldown, corpsStartTime, corpsStacks
    current_time = time.time()
    if corpsStacks < 2 and corpsCooldown >= 35:
        corpsStacks = corpsStacks + 1
        corpsStartTime = time.time()
        print("Corps-a-corps is at ", corpsStacks, " stacks")
    if corpsStacks < 2 and corpsCooldown <= 35:
        corpsCooldown = current_time - corpsStartTime
        print("Corps-a-corps cooldown: ", int(35 - corpsCooldown))
    else:
        print("Corps-a-corps is at ", corpsStacks, " stacks")

def displacement():
    global displacementEngagementCooldown, displacementEngagementStartTime, displacementEngagementStacks
    displacementEngagementStackUpdate()
    if keyboard.is_pressed(displacementInput):
        if displacementEngagementStacks > 0:
            print("Hit Displacement")
            displacementEngagementStacks = displacementEngagementStacks - 1
            displacementEngagementCooldown = 0
            if displacementEngagementStacks == 1:
                displacementEngagementStartTime = time.time()
        else:
            print("Displacement cooldown: ", int(35 - displacementEngagementCooldown))
        print()
        corpsStackUpdate()

def engagement():
    global displacementEngagementCooldown, displacementEngagementStartTime, displacementEngagementStacks
    displacementEngagementStackUpdate()
    if keyboard.is_pressed(engagementInput):
        if displacementEngagementStacks > 0:
            print("Hit Engagement")
            displacementEngagementStacks = displacementEngagementStacks - 1
            displacementEngagementCooldown = 0
            if displacementEngagementStacks == 1:
                displacementEngagementStartTime = time.time()
        else:
            print("Engagement cooldown: ", int(35-displacementEngagementCooldown))
        print()
        corpsStackUpdate()

def displacementEngagementStackUpdate():
    global displacementEngagementCooldown, displacementEngagementStartTime, displacementEngagementStacks
    current_time = time.time()
    if displacementEngagementStacks < 2 and displacementEngagementCooldown >= 35:
        displacementEngagementStacks = displacementEngagementStacks + 1
        displacementEngagementStartTime = time.time()
    if displacementEngagementStacks < 2 and displacementEngagementCooldown <= 35:
        displacementEngagementCooldown = current_time - displacementEngagementStartTime

def displacementEngagementStackUpdatePrint():
    global displacementEngagementCooldown, displacementEngagementStartTime, displacementEngagementStacks
    current_time = time.time()
    if displacementEngagementStacks < 2 and displacementEngagementCooldown >= 35:
        displacementEngagementStacks = displacementEngagementStacks + 1
        displacementEngagementStartTime = time.time()
        print("Displacement and Engagement is at ", displacementEngagementStacks, " stacks")
    if displacementEngagementStacks < 2 and displacementEngagementCooldown <= 35:
        displacementEngagementCooldown = current_time - displacementEngagementStartTime
        print("Displacement and Engagement cooldown: ", int(35 - displacementEngagementCooldown))
    else:
        print("Displacement and Engagement at ", displacementEngagementStacks," stacks")

# Melee Combo Abilities

def riposte():
    global whiteMana, blackMana
    if blackMana >= 20 and whiteMana >= 20:
        print("Hit Enchanted Riposte!")
        blackMana = blackMana - 20
        whiteMana = whiteMana - 20
        addManaStack()
        enchantedRecastWait()
    else:
        print("Hit Riposte!")
        recastWait()

def zwerchhau():
    global whiteMana, blackMana
    if blackMana >= 15 and whiteMana >= 15:
        print("Hit Enchanted Zwerchhau!")
        blackMana = blackMana - 15
        whiteMana = whiteMana - 15
        addManaStack()
        enchantedRecastWait()
    else:
        print("Hit Zwerchhau!")
        recastWait()

def redoublement():
    global whiteMana, blackMana
    if blackMana >= 15 and whiteMana >= 15:
        print("Hit Enchanted Redoublement!")
        blackMana = blackMana - 15
        whiteMana = whiteMana - 15
        addManaStack()
        enchantedRecastWait()
    else:
        print("Hit Redoublement!")
        recastWait()

# Extra methods

def updates():
    accelerationStackUpdatePrint()
    swiftcastUpdatePrint()
    corpsStackUpdatePrint()
    displacementEngagementStackUpdatePrint()
    flecheUpdatePrint()
    contreSixteUpdatePrint()
    printMana()
    print()

def weaves():
    acceleration()
    swiftcast()
    corps()
    displacement()
    engagement()
    fleche()
    contreSixte()

def printMana():
    print("White mana: ", whiteMana)
    print("Black mana: ", blackMana)
    print()


keyboard.add_hotkey(jolt2Input, jolt2)
keyboard.add_hotkey(impactInput, impact)
keyboard.add_hotkey(veraero3Input, veraero3)
keyboard.add_hotkey(veraero2Input, veraero2)
keyboard.add_hotkey(verthunder3Input, verthunder3)
keyboard.add_hotkey(verthunder2Input, veraero2)
keyboard.add_hotkey(verstoneInput, verstone)
keyboard.add_hotkey(verfireInput, verfire)
keyboard.add_hotkey(flecheInput, fleche)
keyboard.add_hotkey(contreSixteInput, contreSixte)
keyboard.add_hotkey(corpsInput, corps)
keyboard.add_hotkey(engagementInput, engagement)
keyboard.add_hotkey(displacementInput, displacement)
keyboard.add_hotkey(swiftcastInput, swiftcast)
keyboard.add_hotkey(accelerationInput, acceleration)
keyboard.add_hotkey(riposteInput, riposte)
keyboard.add_hotkey(zwerchhauInput, zwerchhau)
keyboard.add_hotkey(redoublementInput, redoublement)

keyboard.wait()