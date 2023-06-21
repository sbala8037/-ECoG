from get_frelist import *

from datetime import datetime
from os import listdir
from os.path import isfile, join

def match_mfile(cfg):
    if 'mfile' in cfg:
        return 1, cfg
    Y0, M0, D0, h0, m0 = map(int, datetime.strptime(cfg.date, '%Y-%m-%d %H:%M:%S').strftime('%Y %m %d %H %M').split())
    p = [f for f in listdir(f'C:\\Users\\sbala\\Box\\Srikar\\Baphy\\{cfg.ferret}\\') if not isfile(join(f'C:\\Users\\sbala\\Box\\Srikar\\Baphy\\{cfg.ferret}\\', f))]
    OK = 0
    for i in range(len(p)):
        ff = [f for f in listdir(f'C:\\Users\\sbala\\Box\\Srikar\\Baphy\\{cfg.ferret}\\{p[i]}')]
        for j in range(len(ff)):
            Y1, M1, D1 = map(int, datetime.fromtimestamp(ff[j].st_mtime).strftime('%Y %m %d').split())
            if [Y0, M0, D0] == [Y1, M1, D1]:
                OK = 1
                idx = i
    if not OK:
        return OK, cfg
    P0 = f'C:\\Users\\sbala\\Box\\Srikar\\Baphy\\{cfg.ferret}\\{p[idx]}'
    ff = [f for f in listdir(P0) if f.endswith('.m')]
    tt = []
    for i in range(len(ff)):
        tt.append(list(map(int, datetime.fromtimestamp(ff[i].st_mtime).strftime('%H %M').split())))
    tt = [[x[0] - h0, x[1] - m0] for x in tt]
    tt = [[x[0] * 60 + x[1]] for x in tt]
    mn = min(range(len(tt)), key=lambda i: abs(tt[i][0]))
    cfg.mfile = join(P0, ff[mn])
    return OK, cfg


def get_stimat(cfg):
    print('Loading mfile info ...')
    exec(open(cfg.mfile).read())
    print('Creating stimulus matrix ...')

    if 'NSD' in cfg.mfile:
        sti_mat = get_TS1(cfg.mfile)
        tor_mat = []
        trialLEN = [[i + 1, x.TrialEnd] for i, x in enumerate(sti_mat)]
    else:
        sti_mat, tor_mat, trialLEN = get_frelist(exptevents, exptparams.runclass, exptparams)
    if exptparams.runclass in cfg.experiment:
        cfg.TrialObject = exptparams.TrialObject
        cfg.stimat = sti_mat
        cfg.tormat = tor_mat
        cfg.TrialLen = trialLEN
        cfg.runclass = exptparams.runclass
    elif 'ABA' in cfg.experiment:
        cfg.TrialObject = exptparams.TrialObject
        cfg.stimat = sti_mat
        cfg.tormat = tor_mat
        cfg.TrialLen = trialLEN
        cfg.runclass = exptparams.runclass
    else:
        print(f'experiment: {cfg.experiment}')
        print(f'mfile: {cfg.mfile}')
        print('mfile did not match the experiment, please check...')
    return cfg
