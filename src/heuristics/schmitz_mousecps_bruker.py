"""
Template heudiconv file from
https://neuroimaging-core-docs.readthedocs.io/en/latest/pages/heudiconv.html
"""


def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    from src.heuristics.cfmm_filters.bruker.mt_gre import mt_gre

    # Instantiate all cfmm_filters
    infos = [
        mt_gre(seqinfo).get_info(),
    ]

    # Load all filters into `info`
    info = {}
    for _info in infos:
        info.update(_info)

    return info
