

# (4) Time Integrated Activities

    rpt_db_tac_triexpo --db activities.json -c cycle1


# (3) compute activities in ROIs + INFO

    rpt_db_rois_activity --db db.json -o activities.json
    rpt_db_info --db db.json
    rpt_db_info --db activities.json
    rpt_db_tac_plot --db activities.json -c cycle1

FIXME ==> plot or print or dump as excel ?

# (2) get the time and injection information from the dicom images

    rpt_db_update_spect_info -i BP102_mhd/cycle1/tp1/spect.dcm -c cycle1 -t tp1  --db db.json
    rpt_db_update_spect_info -i BP102_mhd/cycle1/tp2/spect.dcm -c cycle1 -t tp2  --db db.json
    rpt_db_update_spect_info -i BP102_mhd/cycle1/tp3/spect.dcm -c cycle1 -t tp3  --db db.json


# (1) folder structure

We consider the folder structure as follows. The file db.json will contains information about the images, such as the acquisition timing or the activities computed in several ROIs. It is a simple dict structure that can be edited manually or modified by other commands. 
 
    one patient
    │
    ├── db.json                    # database (json): data, timing and activities
    │
    ├── cycle1/
    │   ├── tp1/                   # first timepoint
    │   │   ├── ct.nii.gz          # Original CT image
    │   │   ├── spect.nii.gz       # Original SPECT image
    │   │   ├── rois/              # Segmented ROIs
    │   │   └── ...                # intermediated images (resampled, etc)
    │   │ 
    │   ├── tp2/                   # second timepoint
    │   │   ├── ct.nii.gz          # Original CT image
    │   │   ├── spect.nii.gz       # Original SPECT image
    │   │   ├── rois/              # Segmented ROIs
    │   │   └── ...
    │   
    ├── cycle2/
    │   ├── tp1/                   # first timepoint
    │   └── ...



