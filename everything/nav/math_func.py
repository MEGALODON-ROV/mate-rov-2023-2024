def PWM(joyVal): #converting a double to a PWM value
    Limit = 400 #with 400 the max is 1900 and the min is 1100 PWM
    joyVal = joyVal*Limit
    return joyVal

def makeString(Lx, Ly, Rx, A, B, LeftThrottle, SideThrottle, percent_horiz, percent_vert):
    #Lx-Double/float, Ly-Double/float, Rx-Double/float, A-Boolean, B-Boolean, "Sensitive Mode" - Boolean
    vtr = vtl = vbr = vbl = v2 = fr = fl = br = bl = 1500
    sendStr = "" #constructed string to be sent to the arduino
    capMovement = 400 * (percent_horiz/100)
    capPivot = 400 * (percent_horiz/100)
    Vstrength = 400 * (percent_vert/100)

    # accounting for inverted axis
    Ly = Ly * (-1)  
    Lx = Lx * (1)
    Rx = Rx * (-1)

    # change sign accordingly
    LeftThrottle = LeftThrottle * (1)
    SideThrottle = SideThrottle * (1)
    
    #deadband 0.1 deviation
    if(Lx < 0.1 and Lx > -0.1):
        Lx = 0
    if(Ly < 0.1 and Ly > -0.1):
        Ly = 0


    #LINEAR MODE
    # Front and Back Calculations (cap is 200)
    br += PWM(Ly) * (capMovement/400) 
    bl += PWM(Ly) * (capMovement/400)
    fr += PWM(Ly) * (capMovement/400)
    fl += PWM(Ly) * (capMovement/400)
    

    #Crabbing Calculations (cap is 200)
    br += PWM(Lx)  * (capMovement/400)
    bl += -PWM(Lx) * (capMovement/400)
    fr += -PWM(Lx) * (capMovement/400)
    fl += PWM(Lx)  * (capMovement/400)
    

    #Pivoting CALCULATIONS (cap is 100)
    br += PWM(Rx) * (capPivot/400)
    bl += -PWM(Rx)  * (capPivot/400)
    fr += PWM(Rx) * (capPivot/400)
    fl += -PWM(Rx)  * (capPivot/400)

    # # 1501 = PID ON
    # v1 = v2 = 1501

    #up-down movement
    if(A): #if A is pressed
        vtr += Vstrength
        vtl += Vstrength
        vbr += Vstrength
        vbl += Vstrength
        #v1 and v2 go up
    if(B): #if B is pressed
        vtr -= Vstrength
        vtl -= Vstrength
        vbr -= Vstrength
        vbl -= Vstrength
        #v1 and v2 go down

    vtr -= (LeftThrottle) * Vstrength/4
    vtl -= (LeftThrottle) * Vstrength/4
    vbr += (LeftThrottle) * Vstrength/4
    vbl += (LeftThrottle) * Vstrength/4

    vtr -= (SideThrottle) * Vstrength/4
    vtl += (SideThrottle) * Vstrength/4
    vbr -= (SideThrottle) * Vstrength/4
    vbl += (SideThrottle) * Vstrength/4


    #capping the pwm values at 1900/1100 and round
    pwmArray = [fr, fl, br, bl, vtr, vtl, vbr, vbl]
    for index in range(len(pwmArray)):
        # round to whole number
        pwmArray[index] = round(pwmArray[index])
        pwmArray[index] = max(1100, pwmArray[index])
        pwmArray[index] = min(1900, pwmArray[index])

    #pwmArray[4] = pwmArray[4] 
    # sends the PWM values in the order:
    # fr, fl, br, bl, vtr, vtl, vbr, vbl
    sendStr  = (str(pwmArray[0]) + "-" + 
                str(pwmArray[1]) + "=" + 
                str(pwmArray[2]) + "+" + 
                str(pwmArray[3]) + "*" + 
                str(pwmArray[4]) + "," + 
                str(pwmArray[5]) + "]" +
                str(pwmArray[6]) + "/" +
                str(pwmArray[7]) + "."
                )

    return sendStr