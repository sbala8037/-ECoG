import argparse
from typing import List, Tuple

def load_open_ephys_data(filename: str, indices: List[int] = []) -> Tuple:
    """
    Loads continuous, event, or spike data files into Python.

    Inputs:
        filename: path to file

    Outputs:
        data: either an array continuous samples (in microvolts),
              a matrix of spike waveforms (in microvolts),
              or an array of event channels (integers)

        timestamps: in seconds

        info: structure with header and other information

    Optional Parameter/Value Pairs
        'Indices'   row vector of ever increasing positive integers | []
                    The vector represents the indices for datapoints, allowing
                    partial reading of the file using memmapfile. If empty, all
                    the data points will be returned.

    DISCLAIMER:
        Both the Open Ephys data format and this m-file are works in progress.
        There's no guarantee that they will preserve the integrity of your
        data. They will both be updated rather frequently, so try to use the
        most recent version of this file, if possible.
    """

    # constants
    NUM_HEADER_BYTES = 1024
    SAMPLES_PER_RECORD = 1024
    RECORD_MARKER = [0, 1, 2, 3, 4, 5, 6, 7, 8, 255]
    RECORD_MARKER_V0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 255]

    # constants for pre-allocating matrices:
    MAX_NUMBER_OF_SPIKES = int(1e6)
    MAX_NUMBER_OF_RECORDS = int(1e6)
    MAX_NUMBER_OF_CONTINUOUS_SAMPLES = int(1e8)
    MAX_NUMBER_OF_EVENTS = int(1e6)
    SPIKE_PREALLOC_INTERVAL = int(1e6)

    range_pts = indices

    filetype = filename.split('.')[-1] # parse filetype

    fid = open(filename)
    
    # filesize = getfilesize(fid) # need to implement getfilesize function

    if filetype == 'events':
        
        if range_pts:
            raise ValueError('events data is not supported for memory mapping yet')
        
        print('Loading events file...')
        
        index = 0
        
        hdr = fid.read(NUM_HEADER_BYTES)
        info.header = eval(hdr)
        
        if 'version' in info.header:
            version = info.header['version']
        else:
            version = 0.0
        
        # pre-allocate space for event data
        data = [0] * MAX_NUMBER_OF_EVENTS
        timestamps = [0] * MAX_NUMBER_OF_EVENTS
        info.sampleNum = [0] * MAX_NUMBER_OF_EVENTS
        info.nodeId = [0] * MAX_NUMBER_OF_EVENTS
        info.eventType = [0] * MAX_NUMBER_OF_EVENTS
        info.eventId = [0] * MAX_NUMBER_OF_EVENTS
        