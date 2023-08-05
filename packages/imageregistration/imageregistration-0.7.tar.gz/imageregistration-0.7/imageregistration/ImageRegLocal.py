import subprocess as sub
def ImageRegistration(imagelist, reference):
    """
    Estimates the (affine) transformation matrix between two images. This procedure depends on a server with Mathematica 
    installation. Please note that image transformation might take a while depending on image size. 
    :param reference: path/name to reference image (e.g. ortho foto of an object or overview image) 
    :type reference: string
    :param imagelist: one or more images for transformation procedure
    :type imagelist: list
    
    :returns: only data export
    
    :example:
        >>> 
        
    """
    text_file = open("run_registration.m", "w")
    text_file.write("(* ::Package:: *) \
    (* ::Input:: *) \
    fileName1=ToString[$CommandLine[[4]]]; \
    fileName2=ToString[$CommandLine[[5]]]; \
    imagename1=StringSplit[fileName1,'.'][[1]]; \
    imagename2=StringSplit[fileName2,'.'][[1]]; \
    Needs['GeneralUtilities`'] \
    (* ::Input:: *) \
    ({i1,i2}={Import[fileName1],Import[fileName2]}; \
    y12=ImageCorrespondingPoints[i1,i2]; \
    z12=FindGeometricTransform[y12[[1]], y12[[2]]]; \
    If[Length[y12[[1]]]>1 , \
    {filetemp=y12; \
    Export['TransformMatrix'<>imagename1<>'_'<>imagename2<>'.csv',z12[[2,1]],'CSV']},''];) \
    (* ::Input:: *)")  
    text_file.close()

    for x in range(0, len(imagelist)):
        print('execute script: math -script run_registration.m '+reference[0]+' '+imagelist[x])
        script = 'math -script run_registration.m  '+reference[0]+' '+imagelist[x]
        p = sub.Popen([script],stdout=sub.PIPE,stderr=sub.PIPE) 
    return;
