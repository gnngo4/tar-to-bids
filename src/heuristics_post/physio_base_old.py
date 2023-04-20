import os


def pair_physio_to_mri(
    tar_tree: str, subject_id: str, session_id: str, bids_dir: str
) -> None:
    """
    Relabels physio [.dcm] to
    """

    physio_pairs = _get_physio_pairs(tar_tree)
    _pair_physio_to_mri(tar_tree, physio_pairs, subject_id, session_id, bids_dir)


def _get_physio_pairs(tar_tree: str):
    """
    Naive method to pair physio dcm with corresponding MRI data
    Sequentially matches '_PhysioLog' to MRI data
    Returns a dictionary mapping Physio_log series number to its
    associated MRI series number
    """

    from pydicom import dcmread

    assert (
        tar_tree is not None
    ), "Initialize tar_tree with the reformat_dicom_tree() method."
    series_ids = os.listdir(tar_tree)
    series_ids.sort()  # reorder in ascending order

    # Loop through all SERIES to find SERIES names with a PhysioLog
    track_scans = []
    for series_id in series_ids:
        fp_base = f"{tar_tree}/{series_id}"
        single_dcm = f"{fp_base}/{os.listdir(fp_base)[0]}"
        series_description = dcmread(single_dcm).SeriesDescription
        """
        Associated MRI series_description names can be retrieved 
        from the Physio series description by removing the suffix:
        '_PhysioLog'
        """
        if "_PhysioLog" in series_description:
            track_scans.append(series_description.replace("_PhysioLog", ""))

    physio_idx, physio_pairs = 0, {}
    physio_pair = {"PHYSIO": None, "MRI": None}
    for series_id in series_ids:
        fp_base = f"{tar_tree}/{series_id}"
        single_dcm = f"{fp_base}/{os.listdir(fp_base)[0]}"
        metadata = dcmread(single_dcm)
        series_description = metadata.SeriesDescription
        series_number = metadata.SeriesNumber

        if "_PhysioLog" in series_description:
            physio_pair["PHYSIO"] = str(series_number).zfill(4)
        if track_scans[physio_idx] == series_description:
            physio_pair["MRI"] = str(series_number).zfill(4)

        if physio_pair["PHYSIO"] is not None and physio_pair["MRI"] is not None:
            physio_pairs[physio_pair["PHYSIO"]] = physio_pair["MRI"]  # Add physio match
            physio_pair = {
                "PHYSIO": None,
                "MRI": None,
            }  # Reinitialize `physio_pair` after a match is established
            physio_idx += 1  # Increment `physio_idx`
            # End loop after all `physio_pairs` have been matched
            if physio_idx == len(track_scans):
                break

    return physio_pairs


def _pair_physio_to_mri(
    tar_tree: str,
    physio_pairs: dict,
    subject_id: str,
    session_id: str,
    bids_dir: str,
) -> None:
    """
    Loop through `physio_pairs` and copy physio dicoms to a physio_dir (`physio_dir`)
    """

    physio_dir = f"{bids_dir}/sub-{subject_id}/ses-{session_id}/physio"
    if not os.path.isdir(physio_dir):
        os.mkdir(physio_dir)

    for physio_id, mri_id in physio_pairs.items():
        dcm_physio_dir = f"{tar_tree}/{physio_id}"
        assert (
            len(os.listdir(dcm_physio_dir)) == 1
        ), "Physio dicom folder should contain only 1 file."
        physio_dcm = f"{dcm_physio_dir}/{os.listdir(dcm_physio_dir)[0]}"
        copy_physio_cmd = f"cp {physio_dcm} {physio_dir}/sub-{subject_id}_ses-{session_id}_task-{mri_id}_physio-{physio_id}_PHYSIOLOG.dcm"
        os.system(copy_physio_cmd)
