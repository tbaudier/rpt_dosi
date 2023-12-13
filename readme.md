

# (4) single timepoint dose estimation with Madsen method


    rpt_dose_hanscheid2018 -i spect_Bq.nii.gz -r rois/kidney_left.nii.gz "left kidney" -o a.txt -t 24 --ct ct_2.5mm.nii.gz


# (3) spect and ct pre processing  

TODO : Partial Volume Correction

    rpt_resample_image -i ct.nii.gz -o ct_2.5mm.nii.gz --like spect.nii.gz
    rpt_spect_calibration -i spect.nii.gz -o spect_Bq.nii.gz -c 0.176906614 --concentration
    rpt_spect_calibration -i spect.nii.gz -o spect_Bqml.nii.gz -c 0.176906614


# Get S-values from the Opendose website

They are stored in the data folder.

        opendose_web_get_sources_list -o opendose_sources.json -p "ICRP 110 AM"
        opendose_web_get_isotopes_list -o opendose_isotopes.json -p "ICRP 110 AM"

        opendose_web_get_svalues -r lu177 -s "liver" -p "ICRP 110 AM"
        opendose_web_get_svalues -r lu177 -s "spleen" -p "ICRP 110 AM"
        opendose_web_get_svalues -r lu177 -s "right kidney" -p "ICRP 110 AM"
        opendose_web_get_svalues -r lu177 -s "left kidney" -p "ICRP 110 AM"

        opendose_web_get_sources_list -o opendose_sources.json -p "ICRP 110 AF"     
        opendose_web_get_isotopes_list -o opendose_isotopes.json -p "ICRP 110 AF" 

        opendose_web_get_svalues -r lu177 -s "liver" -p "ICRP 110 AF"               
        opendose_web_get_svalues -r lu177 -s "spleen" -p "ICRP 110 AF"
        opendose_web_get_svalues -r lu177 -s "right kidney" -p "ICRP 110 AF"
        opendose_web_get_svalues -r lu177 -s "left kidney" -p "ICRP 110 AF"


# (2) ROI segmentation

Todo for all images:

    cd cycle1/tp1
    TotalSegmentator -i ct.nii.gz --bs -o rois -ta body 
    TotalSegmentator -i ct.nii.gz --bs -o rois 

FIXME -> for visu, crop is better, do a script to autocrop the images (in separate folder)

The option -fast can be used if too slow. Warning, a GPU is highly advised.

# (1) convert DICOM to mhd (manual for the moment)

Exemple of DICOM conversion, adapt the folder/filenames to your own data: 

    # CT
    gt_image_convert BP102/CT/Other_/20231012/142513.288/1.250000E+00/soft_tissue_H4_C1_/*dcm -o BP102_mhd/cycle1/tp1/ct.nii.gz -v
    gt_image_convert BP102/CT/Other_/20231013/090804.208/1.250000E+00/soft_tissue_/*dcm -o BP102_mhd/cycle1/tp2/ct.nii.gz -v
    gt_image_convert BP102/CT/Other_/20231018/091617.804/1.250000E+00/soft_tissue_/*dcm -o BP102_mhd/cycle1/tp3/ct.nii.gz -v

    # SPECT
    gt_image_convert BP102/NM/Lu177-PSMA/20231012/142334.000/2.46/7_FFS_LU177_OSAC_Recon_Patient1_ScC_/*.dcm -o BP102_mhd/cycle1/tp1/spect.nii.gz
    gt_image_convert BP102/NM/Lu177-PSMA/20231013/090544.000/2.46/7_FFS_LU177_OSAC_Recon_Patient1_ScC_/*.dcm -o BP102_mhd/cycle1/tp2/spect.nii.gz
    gt_image_convert BP102/NM/Lu177-PSMA/20231018/091324.000/2.46/7_FFS_LU177_OSAC_Recon_Patient1_ScC_/*.dcm -o BP102_mhd/cycle1/tp3/spect.nii.gz

    # visu 
    vv BP102_mhd/cycle1/tp1/ct.nii.gz --fusion BP102_mhd/cycle1/tp1/spect.nii.gz BP102_mhd/cycle1/tp2/ct.nii.gz --fusion BP102_mhd/cycle1/tp2/spect.nii.gz BP102_mhd/cycle1/tp3/ct.nii.gz --fusion BP102_mhd/cycle1/tp3/spect.nii.gz 

We consider the folder structure as follows:
  
    patient (named BP102_mhd here)
    │
    ├── cycle1/
    │   ├── tp1/                   # first timepoint
    │   │   ├── ct.nii.gz          # Original CT image
    │   │   ├── spect.nii.gz       # Original SPECT image
    │   │   └── rois/              # Segmented ROIs
    │   ├── tp2/
    │   │   ├── ct.nii.gz          # Original CT image
    │   │   ├── spect.nii.gz       # Original SPECT image
    │   │   └── rois/              # Segmented ROIs
    │   └── ...
    ├── cycle2/
    │   ├── tp1/                   # first timepoint
    │   └── ...

