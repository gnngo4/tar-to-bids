"""
Template heudiconv file from
https://neuroimaging-core-docs.readthedocs.io/en/latest/pages/heudiconv.html
"""


def pop_item_from_infos(infos, task_id, part, pop_idx, sbref=False):
    for i, j in infos.items():
        try:
            if sbref:
                _task_id = i[0].split("task-")[1].split("_")[0]
                _suffix = i[0].split("_")[-1]
                if _task_id == task_id and _suffix == "sbref":
                    return j.pop(pop_idx)
            else:
                _task_id = i[0].split("task-")[1].split("_")[0]
                _part = i[0].split("part-")[1].split("_")[0]
                if _task_id == task_id and _part == part:
                    return j.pop(pop_idx)
        except:
            continue

    assert False, f"Nothing happened."


def add_item_to_infos(infos, item, task_id, part, sbref=False):
    for i, j in infos.items():
        try:
            if sbref:
                _task_id = i[0].split("task-")[1].split("_")[0]
                _suffix = i[0].split("_")[-1]
                if _task_id == task_id and _suffix == "sbref":
                    j.append(item)
                    infos[i] = sorted(j, key=lambda k: k["item"])
                    return infos

            else:
                _task_id = i[0].split("task-")[1].split("_")[0]
                _part = i[0].split("part-")[1].split("_")[0]
                if _task_id == task_id and _part == part:
                    j.append(item)
                    infos[i] = sorted(j, key=lambda k: k["item"])
                    return infos
        except:
            continue

    assert False, f"Nothing happened."


def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    from src.heuristics.cfmm_filters.three_tesla.mprage import mprage
    from src.heuristics.cfmm_filters.three_tesla.gre_field_map import (
        gre_field_map,
    )
    from src.heuristics.cfmm_filters.three_tesla.schmitz_osc_3t_v1 import (
        bold,
    )

    # Instantiate all cfmm_filters
    infos = [
        mprage(seqinfo).get_info(),
        gre_field_map(seqinfo).get_info(),
        bold(seqinfo).get_info(),
    ]

    patient_id = seqinfo[0].patient_id
    print(f"PATIENT ID: {patient_id}")
    if patient_id == "2022_11_04_T009_S001":
        _ = [print(f"\n\n{i[0]}\n{j}") for i, j in infos[2].items()]
        _item = pop_item_from_infos(infos[2], "prfMultibar", "mag", 1)
        infos[2] = add_item_to_infos(infos[2], _item, "prfExpand", "mag")
        _item = pop_item_from_infos(infos[2], "prfMultibar", "phase", 1)
        infos[2] = add_item_to_infos(infos[2], _item, "prfExpand", "phase")
    if patient_id == "2023_02_22_T005_S001":
        _ = [print(f"\n\n{i[0]}\n{j}") for i, j in infos[2].items()]
        _item = pop_item_from_infos(infos[2], "localizerQ2", "mag", 0)
        _item = pop_item_from_infos(infos[2], "localizerQ2", "phase", 0)
        _item = pop_item_from_infos(infos[2], "localizerQ2", None, 0, sbref=True)
    if patient_id == "2023_03_29_T006_S002":
        _ = [print(f"\n\n{i[0]}\n{j}") for i, j in infos[2].items()]
        _item = pop_item_from_infos(infos[2], "controlQ2", "mag", 2)
        infos[2] = add_item_to_infos(infos[2], _item, "entrainQ2", "mag")
        _item = pop_item_from_infos(infos[2], "controlQ2", "phase", 2)
        infos[2] = add_item_to_infos(infos[2], _item, "entrainQ2", "phase")
        _item = pop_item_from_infos(infos[2], "controlQ2", None, 2, sbref=True)
        infos[2] = add_item_to_infos(infos[2], _item, "entrainQ2", None, sbref=True)

    _ = [print(f"\n\n{i[0]}\n{j}") for i, j in infos[2].items()]

    # Load all filters into `info`
    info = {}
    for _info in infos:
        info.update(_info)

    return info
