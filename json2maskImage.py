#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 17:25:52 2018

@author: shariba
"""
def check(list1, val): 
    return(all(x > val for x in list1)) 
    
def check_less(list1, val): 
    return(all(x < val for x in list1)) 
    
def clearArray (xval_artefact, yval_artefact, w, s):
    j2=0
    if (s =='height'):
        for i in range (len(xval_artefact)):
            if (check_less(xval_artefact[i], w) == False ):
                j2 = list(filter(lambda x: x > w, xval_artefact[i]))
                for j in range (len(j2)):
                    ind=xval_artefact[i].index(j2[j])
                    del xval_artefact[i][ind]
                    del yval_artefact[i][ind]   
    else:
        for i in range (len(yval_artefact)):
            if (check_less(yval_artefact[i], w) == False):
                j2 = list(filter(lambda x: x > w, yval_artefact[i]))      
#        j3 = list(filter(lambda x: x > h, yval_artefact[i]))
                for j in range (len(j2)):
                    ind=yval_artefact[i].index(j2[j])
                    del xval_artefact[i][ind]
                    del yval_artefact[i][ind]   
                
    return xval_artefact, yval_artefact

def clearArray_zeroBound (xval_artefact, yval_artefact, val):
    for i in range (len(xval_artefact)):
#        check if its greater than certain value
        if (check(xval_artefact[i], val) == False or check(yval_artefact[i], val) == False):
            j2 = list(filter(lambda x: x < val, xval_artefact[i]))
            for j in range (len(j2)):
                ind=xval_artefact[i].index(j2[j])
                del xval_artefact[i][ind]
                del yval_artefact[i][ind]
                
            j3 = list(filter(lambda x: x < val, yval_artefact[i]))
            for j in range (len(j3)):
                ind=yval_artefact[i].index(j3[j])
                del xval_artefact[i][ind]
                del yval_artefact[i][ind]
                
    return xval_artefact, yval_artefact

#            
#        for j in range (len(j3)):
#            ind=yval_artefact[i].index(j3[j])
#            del xval_artefact[i][ind]
#            del yval_artefact[i][ind] 

def draw_caption(image, boxes):
    import random as rnd
    import cv2
    value = [rnd.randint(0, 255), rnd.randint(0, 255), rnd.randint(0, 255)]
    
    cv2.putText(image, boxes[0], (boxes[1], boxes[2] - 10), cv2.FONT_HERSHEY_PLAIN, 1, value, 1)
    cv2.rectangle(image, (boxes[1], boxes[2]), (boxes[3], boxes[4]), color=value, thickness=2)
    return image

    
def read_json_file(jsonFile):
    import json
    import objectpath
    category = []
    bbox = []
    segment=[]
    result_tuple_from_segment=[]
    with open(jsonFile) as json_data:
        data = json.load(json_data)
#        print(data)
        for p in data["layers"]:
            if len(p['items'])!=0:
                category.append(p['name'])
#                loop for the items
                for l in range (len(p['items'])):
                    jsonnn_tree = objectpath.Tree(p['items'][l])
                    result_tuple_from = tuple(jsonnn_tree.execute('$..from'))
                    result_tuple_to = tuple(jsonnn_tree.execute('$..to'))
                    #annotation points here
                    result_tuple_from_segment = tuple(jsonnn_tree.execute('$..point'))
                    segment.append(result_tuple_from_segment)
                    xbottom=json.dumps(result_tuple_from)
                    bottom = re.findall("\d+\.\d+", xbottom)
                    
                    if len(bottom)>2:
                        for k in range ((int)(len(bottom)/2)-1):
                            category.append(p['name'])
                    
                    if l >1:
                        category.append(p['name'])
                            
                    bbox.append(result_tuple_from)
                    bbox.append(result_tuple_to)
       
    return category, bbox, data, segment



def read_json_file_admin(jsonFile):
    import json
    import objectpath
    category = []
    bbox = []
    segment=[]
    with open(jsonFile) as json_data:
        data = json.load(json_data)
        X=data["annotation"]
        imageName=data["images"]
        frameName=imageName[0].get('name')
        for p in X["layers"]:
            if len(p['items'])!=0:
                category.append(p['name'])
                jsonnn_tree = objectpath.Tree(p['items'])
                result_tuple_from = tuple(jsonnn_tree.execute('$..from'))
                result_tuple_to = tuple(jsonnn_tree.execute('$..to'))
                
                if result_tuple_from == []:
                    result_tuple_from = tuple(jsonnn_tree.execute('$..point'))
                xbottom=json.dumps(result_tuple_from)
                bottom = re.findall("\d+\.\d+", xbottom)
                if len(bottom)>2:
                    for k in range ((int)(len(bottom)/2)-1):
                        category.append(p['name'])
                bbox.append(result_tuple_from)
                #annotation points here
                if result_tuple_from == []: 
                    segment.append(result_tuple_from)
                else:
                    bbox.append(result_tuple_to) 
    return category, bbox, frameName, data, segment

def saveAnnotationMaskImage(img, xval_artefact, yval_artefact, category, maskImageFileName):
    '''
    saves annotation only with class boundaries (produces single image file) 
    
    '''
    img=img[:,:,[2,1,0]]
    [height, width, ch] = img.shape
    maskImage=np.zeros((height,width,ch), np.uint8)
    dpi = 80
    figsize = width / float(dpi), height / float(dpi)
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    ax.imshow(maskImage, interpolation='nearest')
    for i in range (len(xval_artefact)):
        plt.plot(xval_artefact[i][:],yval_artefact[i][:], linewidth=2)    
    ax.axis('image')
    ax.set(xlim=[0, width], ylim=[height, 0], aspect=1)
    fig.savefig(maskImageFileName, dpi=dpi, transparent=True)
    plt.show() 
    
    
def saveAnnotationMasksPerClass(img, xval_artefact, yval_artefact, category, maskImageFileName):
    '''
    saves annotation masks per class 
    multi-class annotations are marked with _#
    '''
    img=img[:,:,[2,1,0]]
    [height, width, ch] = img.shape
    maskImage=np.zeros((height,width,ch), np.uint8)
    colorArray = ['red', 'green', 'magenta', 'cyan', 'blue', '']
    dpi = 80
    figsize = width / float(dpi), height / float(dpi)
    maskImageFileName_class = maskImageFileName.split('.')[0]
    unique_entries = set(category)
#    convert set to list 
#    list_uniqueClasses = list(unique_entries)
    
    indices = { value : [ i for i, v in enumerate(category) if v == value ] for value in unique_entries }
    arrayList_cat= []
    for k in range (len(unique_entries)):
        arrayList_cat.append(len(indices[category[k]]))
    
#    print(arrayList_cat)
    maskImageFileNameList = []
    
    for i in range (len(unique_entries)):
        fig = plt.figure(figsize=figsize)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        ax.imshow(maskImage, interpolation='nearest')
        ax.axis('image')
        ax.set(xlim=[0, width], ylim=[height, 0], aspect=1)
        j = 0
        plt_before = plt.fill(0,0, linewidth=5,color=colorArray[i])
#        combine masks belonging to same class
#        while j <= arrayList_cat[i]:
    #        plt.plot(xval_artefact[i][:],yval_artefact[i][:], linewidth=5,color=colorArray[i])
        k = indices.get(category[i])
        l = k[0]
        if len(k) == 1:
            plt.fill(xval_artefact[l][:],yval_artefact[l][:], linewidth=5,color=colorArray[i])
        else: 
#            TODO: There was a mistake in Barbara's annotation for 01440.jpg (consisted of empty arrays for last case)
            while j < len(k):
                l = k[j]
                print(k[j])
                plt_before=plt_before+plt.fill(xval_artefact[l][:],yval_artefact[l][:], linewidth=5,color=colorArray[i])
                j += 1
       
#        if annotation outside box then delete it    
        maskImageFileName = maskImageFileName_class+'_'+category[i]+'.png'
        print(maskImageFileName)
        fig.savefig(maskImageFileName, dpi=dpi, transparent=True)
        maskImageFileNameList.append(maskImageFileName)
        
    return maskImageFileNameList
        
#    fi.write_multipage(image, 'test_multiple.tif')
#    plt.show() 
    
useParsing=0
debug = 0
writeImagewithBox=1
annotator=['adam', 'barbara']

if __name__=="__main__":

    import re
    import argparse
    
    artefactsList=[]
 
    file = ''
    
    if useParsing:
    
        parser = argparse.ArgumentParser()
        parser.add_argument('-jsonFileName', action='store', help='please include the full path of the folder with bounding boxes (.json)', type=str)
        parser.add_argument('-imageFileName', action='store', help='folder only (fullpath)', type=str)
        args = parser.parse_args()
    
        jsonFile=args.jsonFileName
        imageFile = args.imageFileName
        
#        uncomment and use this if you are using the annotation from json file directly from the annotator source
#        category,  bbox = read_json_file(jsonFile)
        
#        use below if you are using the file downloaded from the admin (only save most recent json files--> convert to proper json format)
#        category,  bbox, frameName, data = read_json_file_admin(jsonFile)
        category,  bbox, data, segment = read_json_file(jsonFile)
         
#        file = txtFolder+frameName+annotator[0]+'.txt'
#        jsonFileRenamed=txtFolder+frameName+'_'+annotator[0]+'.json'
        
        frameName=imageFile.split('.')[0]
        
#        fileObj= open(jsonFileRenamed, "w")
#        json.dump(data, fileObj)
#        fileObj.close()
#        also save the json file with annotator name and corresponding file name
        
        
    else:
        print('testing with some test file...')
#        jsonFile='AIDA_annotation-2.json'//data can be deprecated
        jsonFile='AIDA_barbara_2233.json'
        jsonFile='sampleJson/AIDA_annotation-3_barbara_2233.json'
#        jsonFile='sampleJson/AIDA_annotation_1440.json'
#        TODO admin
#        category,  bbox, frameName, data = read_json_file_admin(jsonFile)
        category,  bbox, data, segment = read_json_file(jsonFile)
        frameName='Frame_00002233' 
#        frameName='01440' 


# do for above params
'''
    Extract x-, y- indices from json file
'''        
xval_artefact=[]
yval_artefact=[]

for i in range (len(segment)):
    xvals=[]
    yvals=[]
    for j in range (len(segment[i])):
        temp=segment[i][j]
        xvals.append(int(temp.get('x')))
        yvals.append(int(temp.get('y')))
        
    xval_artefact.append(xvals)
    yval_artefact.append(yvals)


'''
    Call correponding image and create masks with above array list of indices
'''
import cv2 
import numpy as np
import matplotlib.pyplot as plt

annotationImage='annotation_image/'+frameName+'.jpg'
maskImageName=frameName+'_mask.jpg'
img = cv2.imread(annotationImage, 1)
img=img[:,:,[2,1,0]]

'''
    Delete empty entries in the array
    TODO: count no of empty entries 
'''
xval_artefact = list(filter(None, xval_artefact))
yval_artefact = list(filter(None, yval_artefact))
'''
    Annotation boundary handling 
'''
#zero-val boundary keep only >0 indices
xval_artefact, yval_artefact= clearArray_zeroBound (xval_artefact, yval_artefact, 0)          
h, w, ch = img.shape
# keep only <=h and <=w indices
xval_artefact, yval_artefact= clearArray (xval_artefact, yval_artefact, h, 'width')  
xval_artefact, yval_artefact= clearArray (xval_artefact, yval_artefact, w, 'height')       

'''
    Create annotation masks and save them
'''
# saveAnnotationMaskImage(img, xval_artefact, yval_artefact, category, maskImageName)
maskImageFileNameList=saveAnnotationMasksPerClass(img, xval_artefact, yval_artefact, category, maskImageName)

# save annotation masks as binary 7 channel masks? (0, 1, 2, 3, 4, 5, 6)

# save as tiff images
# testing
'''
       1) make an empty array of size [h, w, #classes]
        2) masks per class type (check before each indexing)
        3) save array as tif [array]
'''
import PIL 
from PIL import Image

list_file=maskImageFileNameList
# write ordered maskImageList in txt file
textfile = open(frameName+'_mask.txt', 'a')

# mask list 
with PIL.TiffImagePlugin.AppendingTiffWriter(frameName+'_mask.tiff',True) as tf:        
    for i in range (len(list_file)):
        tiff_in=list_file[i]
        im= Image.open(tiff_in).convert('L')
        im.save(tf)
        tf.newFrame()
        textfile.write(tiff_in)
        textfile.write('\n')
        
textfile.close()
            
'''
    Experimental codes only
'''

unique_entries = set(category)
indices = { value : [ i for i, v in enumerate(category) if v == value ] for value in unique_entries }


