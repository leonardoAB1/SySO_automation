# [Worker-Safety - v1 WorkerSafety  ](https://universe.roboflow.com/computer-vision/worker-safety)

------------------------------------------------------------------------------------

This dataset was exported via roboflow.com.

Roboflow is an end-to-end computer vision platform that helps you  
* collaborate with your team on computer vision projects  
* collect & organize images  
* understand unstructured image data  
* annotate, and create datasets  
* export, train, and deploy computer vision models  
* use active learning to improve your dataset over time  

It includes 3200 images.  
Helmet are annotated in Pascal VOC format.  

The following pre-processing was applied to each image:  
* Auto-orientation of pixel data (with EXIF-orientation stripping)  
* Resize to 416x416 (Stretch)  
  
The following augmentation was applied to create 3 versions of each source image:  
* Equal probability of one of the following 90-degree rotations: none, clockwise, counter-clockwise, upside-down  
* Random rotation of between -15 and +15 degrees  
* Random shear of between -15° to +15° horizontally and -15° to +15° vertically  
* Random Gaussian blur of between 0 and 2 pixels  
* Salt and pepper noise was applied to 10 percent of pixels  