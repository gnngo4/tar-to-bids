import os

from src.heuristics_post.physio_base_old import pair_physio_to_mri
from src.csv_reader.tar_mapper import task_mapper


def annotate_func(subject: str, session: str, bids_dir: str) -> None:
    # Get all files in physio and func directory
    physio_ls = _bids_listdir("physio", subject, session, bids_dir)
    func_ls = _bids_listdir("func", subject, session, bids_dir)
    """
    Aggregate files in `func_ls` and `physio_ls`
    (1) Within a series_id, aggregation will have one of the following:
        '.json', 'events.tsv', 'bold.nii.gz',
    (2) Aggregate sbref to each mapping sequentially based on series_id order
    (3) Aggregate physio data to each mapping based on series_id
    """
    func_ls, func_runs = _aggregate_bold(func_ls)
    func_ls, func_runs = _aggregate_sbref(func_ls, func_runs)
    physio_ls, func_runs = _aggregate_physio(physio_ls, func_runs)

    return func_runs, func_ls, physio_ls


def log_and_clean_unmapped_func(func_ls, physio_ls, subject_id, session_id, bids_dir):
    import shutil

    print("\nThe following files were not converted:")
    for i in func_ls:
        print(f"FUNC     : {i}")
        os.remove(i)
    for i in physio_ls:
        print(f"PHYSIO   : {i}")
    physio_dir = f"{bids_dir}/sub-{subject_id}/ses-{session_id}/physio"
    shutil.rmtree(physio_dir)


def remap_func(func_runs, task_mappings):
    # Remapping
    event_runs = {}
    print("\nRemapping:")
    for series_id, f in func_runs.items():
        print(f"Series ID: {series_id}")
        task_event = task_mappings.get(series_id)
        if event_runs.get(task_event) is None:
            event_runs[task_event] = 1
        else:
            event_runs[task_event] += 1
        for _type, _f in f.items():
            if _f is not None:
                _series_id = _f.split("task-")[1][:4]
                relabel_f = _f.replace(
                    f"task-{_series_id}", f"task-{task_event}"
                ).replace(
                    "run-01",
                    f"run-{str(event_runs[task_event]).zfill(2)}",
                )
                # quick-fix for relabeling of physio[.dcm]
                if _type == "physio":
                    physio_idx = relabel_f.index("physio-")
                    physio_id = relabel_f[physio_idx : physio_idx + 12]
                    suffix = (
                        f["mag_bold"]
                        .split("_acq")[1]
                        .replace("nii.gz", "dcm")
                        .replace(
                            "run-01",
                            f"run-{str(event_runs[task_event]).zfill(2)}",
                        )
                    )
                    suffix = suffix.replace("part-mag", "part-mag_desc-physio")
                    relabel_f = (
                        relabel_f.replace("/physio/", "/func/")
                        .replace(physio_id, "")
                        .replace("PHYSIOLOG.dcm", f"acq{suffix}")
                    )
                print(f"{_f} -> {relabel_f}")
                os.rename(_f, relabel_f)
    print("\n")


def heudiconv_post_process(
    tar_tree: str,
    subject_id: str,
    session_id: str,
    bids_dir: str,
    heuristic: str,
    task_mapping: str,
):
    pair_physio_to_mri(tar_tree, subject_id, session_id, bids_dir)
    task_mappings = task_mapper(
        heuristic.replace(".py", ""), task_mapping
    ).get_series_to_task_mappings()
    func_runs, func_ls, physio_ls = annotate_func(subject_id, session_id, bids_dir)
    remap_func(func_runs, task_mappings)
    log_and_clean_unmapped_func(func_ls, physio_ls, subject_id, session_id, bids_dir)


def _aggregate_bold(func_ls):
    func_runs = {}
    for f in func_ls[:]:
        series_id = f.split("task-")[1][:4]

        suffix = "bold.json"
        if suffix == f[-len(suffix) :]:
            if func_runs.get(series_id) is None:
                func_runs[series_id] = _set_run()
            func_runs[series_id]["json_bold"] = f
            func_ls.remove(f)

        suffix = "bold.nii.gz"
        if suffix == f[-len(suffix) :]:
            if func_runs.get(series_id) is None:
                func_runs[series_id] = _set_run()
            func_runs[series_id]["mag_bold"] = f
            func_ls.remove(f)

        suffix = "events.tsv"
        if suffix == f[-len(suffix) :]:
            if func_runs.get(series_id) is None:
                func_runs[series_id] = _set_run()
            func_runs[series_id]["events_tsv"] = f
            func_ls.remove(f)

    return func_ls, func_runs


def _aggregate_sbref(func_ls, func_runs):
    for f in func_ls[:]:
        suffix = "sbref.json"
        if suffix == f[-len(suffix) :]:
            for series_id, j in func_runs.items():
                base = j.get("mag_bold").split("acq-")[1].split("_part-")[0]
                base_f = f.split("acq-")[1].split("_part-")[0]
                if base_f != base:
                    continue
                if j.get("json_sbref") is None:
                    j["json_sbref"] = f
                    break
            func_ls.remove(f)

        suffix = "sbref.nii.gz"
        if suffix == f[-len(suffix) :]:
            for series_id, j in func_runs.items():
                base = j.get("mag_bold").split("acq-")[1].split("_part-")[0]
                base_f = f.split("acq-")[1].split("_part-")[0]
                if base_f != base:
                    continue
                if j.get("mag_sbref") is None:
                    j["mag_sbref"] = f
                    break
            func_ls.remove(f)

    return func_ls, func_runs


def _aggregate_physio(physio_ls, func_runs):
    for f in physio_ls[:]:
        series_id = f.split("task-")[1][:4]

        suffix = "PHYSIOLOG.dcm"
        if suffix == f[-len(suffix) :]:
            if func_runs.get(series_id) is None:
                continue
            func_runs[series_id]["physio"] = f
            physio_ls.remove(f)

    return physio_ls, func_runs


def _bids_listdir(dir_type: str, subject_id: str, session_id: str, bids_dir: str):
    base_dir = f"{bids_dir}/sub-{subject_id}/ses-{session_id}/{dir_type}"
    assert os.path.isdir(base_dir), f"Directory: [{base_dir}] does not exist."

    filtered_list = []
    for i in os.listdir(base_dir):
        series_id = i.split("task-")[1][:4]
        try:
            series_id = int(series_id)
            filtered_list.append(i)
        except:
            continue

    list_dir = [f"{base_dir}/{i}" for i in filtered_list]
    list_dir.sort()

    return list_dir


def _set_run():
    return {
        "json_bold": None,
        "mag_bold": None,
        "events_tsv": None,
        "json_sbref": None,
        "mag_sbref": None,
        "physio": None,
    }
