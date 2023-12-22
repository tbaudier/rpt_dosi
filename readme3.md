

# (2) print series and select

    rpt_dicom_select -i dicom/BM11/dicomdir.json -f -d ScC


# (1) dicom analysis 

The following command lines analyse a folder that contains DICOM files and store a json file with the list of series/studies. This json file will be used to print and select the files. 

    # for one single folder 
    rpt_dicom_browse -i dicom/BC4 -o dicom/BC4/dicomdir.json

    # for all folders 
    rpt_dicom_browse -i dicom -o dicomdir.json -r
    