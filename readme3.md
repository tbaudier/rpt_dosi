

# (2) print series, select and convert dicoms

    # select the dicoms (one by one, manually)
    rpt_dicom_select -i dicom/BC4/dicomdir.json -f -d ScC -o dicom/BC4/selected.json
    
    # convert to nii and create the db ; add -r option to run the conversion
    rpt_dicom_db -i dicom/BC4/selected.json -o BC4

Current status

              select  convert   TotSeg  dates   activities
      BC4     X         X       wip
      BF43    X         
      BM11   
      BP102  
      CP7    
      DG8    
      DL6    
      DY^^2  
      FD3    
      GC^^   
      GP3    
      LM10   
      LM^^2  
      LM^^22 
      MD^^   
      PA8



# (1) dicom analysis 

The following command lines analyse a folder that contains DICOM files and store a json file with the list of series/studies. This json file will be used to print and select the files. 

    # for one single folder 
    rpt_dicom_browse -i dicom/BC4 -o dicom/BC4/dicomdir.json

    # for all folders 
    rpt_dicom_browse -i dicom -o dicomdir.json -r
    