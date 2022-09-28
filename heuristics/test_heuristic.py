'''
Template heudiconv file from
https://neuroimaging-core-docs.readthedocs.io/en/latest/pages/heudiconv.html
'''

def hi():
    print('hi')

def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    # Add to module search path
    import sys
    sys.path.append('/heuristics')

    from cfmm_filters.seven_tesla.mp2rage import mp2rage

    # Track mp2rage
    info = mp2rage(seqinfo).get_info()

    # info1.update(info2)

    return info