'''
Template heudiconv file from
https://neuroimaging-core-docs.readthedocs.io/en/latest/pages/heudiconv.html
'''

def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    from cfmm_filters import mp2rage_7T
    info = mp2rage_7T(seqinfo).get_info()

    return info