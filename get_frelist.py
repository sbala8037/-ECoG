def get_frelist(exptevents, runclass, exptparams=None):
    s = []
    stor = []
    trialLEN = []
    NOTAR = []
    reward = []
    STIMULATION = 0
    dbAtten = []
    if runclass.lower() == 'rts':
        runclass_sub = exptparams.TrialObject.ReferenceHandle.Type
    else:
        runclass_sub = ''
    for i in range(len(exptevents)):
        tem = exptevents[i]
        if 'stimulation' in exptevents[i].Note.lower():
            STIMULATION = 1
        elif exptevents[i].Note.lower() == 'stim,off':
            NOTAR.append(exptevents[i])
        elif exptevents[i].Note[:4].lower() == 'stim' and runclass_sub.lower() == '3stream':
            tem.target = exptevents[i].Note.lower().count('target')
            tem1 = exptevents[i].Note.split(',')
            tem1[1] = tem1[1].replace('Note', '')
            tem.Note = int(tem1[1])
            if len(tem.Note) == 1:
                tem.Note.append(float('nan'))
            s.append(tem)
        elif exptevents[i].Note[:4].lower() == 'stim' and 'note' in exptevents[i].Note.lower():
            tem.target = exptevents[i].Note.lower().count('target')
            if runclass.lower() == 'vbn':
                tem1 = exptevents[i].Note.split(',')
                tem.Note = int(tem1[1].replace('Note', ''))
            else:
                tem1 = exptevents[i].Note.split()
                if runclass.lower() == 'rts':
                    tem.Note = int(tem1[3].split('_')[0])
                else:
                    tem.Note = int(tem1[3].replace('$', ''))
            s.append(tem)
        elif exptevents[i].Note[:4].lower() == 'stim' and runclass.lower() in ['ftc', 'mrd']:
            tem.target = exptevents[i].Note.lower().count('target')
            tem1 = exptevents[i].Note.split(',')
            tem.Note = int(tem1[1])
            if runclass.lower() == 'mrd':
                if len(tem1) == 4:
                    dbAtten.append(int(tem1[3]))
                else:
                    dbAtten.append(0)
            s.append(tem)
        elif exptevents[i].Note[:4].lower() == 'stim' and runclass.lower() in ['ptd', 'tst', 'cch', 'fms', 'fmd', 'clt', 'clk'] and 'torc' not in exptevents[i].Note.lower():
            tem.target = exptevents[i].Note.lower().count('target')
            tem1 = exptevents[i].Note.split(',')
            if 'fm' in tem1[1]:
                fs, fe = map(int, tem1[1][2:].split('-'))
                tem.Note = [fs, fe]
            elif runclass.lower() in ['fms', 'fmd'] and 'silence' not in tem1[1]:
                fs, fe = map(int, tem1[1].replace('$', '').split('-'))
                tem.Note = [fs, fe]
            else:
                if 'silence' in tem1[1]:
                    F_tem = float('nan')
                else:
                    F_tem = int(tem1[1])
                if runclass.lower() == 'fmd':
                    tem.Note = [F_tem, float('nan')]
                else:
                    tem.Note = F_tem
                    if len(F_tem) == 2:
                        tem.Atten = F_tem[1]
                    else:
                        tem.Atten = float('nan')
            s.append(tem)
        elif exptevents[i].Note[:4].lower() == 'stim' and runclass.lower() in ['pfs', 'srv', 'rts', 'mvc', 'voc', 'nse', 'sp1', 'wrd', 'abx', 'xyx', 'srh']:
            tem.target = exptevents[i].Note.lower().count('target')
            tem1 = exptevents[i].Note.split(',')
            tem.Note = tem1[1]
            if runclass.lower() == 'xyx':
                tem.trigger = exptevents[i].Note.lower().count('trigger')
            if len(tem1) > 3:
                tem.Atten = int(tem1[-1].replace('dB', ''))
            else:
                tem.Atten = 0
            s.append(tem)
        elif exptevents[i].Note[:4].lower() == 'stim' and ('torc' in exptevents[i].Note.lower() or 'ferret' in exptevents[i].Note.lower()):
            tem.target = exptevents[i].Note.lower().count('target')
            tem1 = exptevents[i].Note.split(',')
            if '.wav' in tem.Note:
                tem.Note = int(tem1[3])
            else:
                tem.Note = int(tem1[1][9:11])
            if tem1[2].lower() == 'target':
                tem.Note += 30
            stor.append(tem)
        elif exptevents[i].Note.lower() == 'trialstop':
            trialLEN.append(exptevents[i])
        elif 'behavior,pumpon' in exptevents[i].Note.lower():
            reward.append([exptevents[i].Trial, exptevents[i].StartTime, exptevents[i].StopTime])
    if STIMULATION:
        if dbAtten:
            dbAtten = [x for i, x in enumerate(dbAtten) if s[i].target]
        s = [x for x in s if not x.target]
    trialLEN = [[x.Trial, x.StartTime] for x in trialLEN]
    if runclass.lower() == 'rts':
        if exptparams.TrialObject.ReferenceHandle.Type.lower() == 'new_daniel':
            stiname = exptparams.TrialObject.ReferenceHandle.Names
            ss = []
            for i in range(len(s)):
                a1, a2, a3 = map(int, s[i].Note.split('-'))
                a1 = [i for i, x in enumerate(stiname) if x.lower() == a1.lower()][0]
                ss.append([s[i].Trial, a1, s[i].StartTime, s[i].StopTime, a2, a3])
            s = ss
            s[:, 2:4] *= 1000
            return s
        elif exptparams.TrialObject.ReferenceHandle.Type.lower() == 'rshepard':
            for i in range(len(s)):
                ss = s[i].Note.strip()
                s[i].Note = int(ss[-2:])
        elif exptparams.TrialObject.ReferenceHandle.Type.lower() == 'oddball2':
            ss[:, 0] = [x.Trial for x in s]
            ss[:, 2] = [x.StartTime for x in s]
            ss[:, 3] = [x.StopTime for x in s]
            ss[:, 4:7] = [x.Note for x in s]
