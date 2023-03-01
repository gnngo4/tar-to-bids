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

    from src.heuristics.cfmm_filters.seven_tesla.mp2rage import mp2rage
    from src.heuristics.cfmm_filters.seven_tesla.sa2rage import sa2rage
    from src.heuristics.cfmm_filters.seven_tesla.gre_field_map import gre_field_map
    from src.heuristics.cfmm_filters.seven_tesla.schmitz_att_v1 import bold

    # Instantiate all cfmm_filters
    infos = [
        mp2rage(seqinfo).get_info(),
        sa2rage(seqinfo).get_info(),
        gre_field_map(seqinfo).get_info(),
        bold(seqinfo).get_info(),
    ]

    # Load all filters into `info`
    info = {}
    for _info in infos:
        info.update(_info)

    return info