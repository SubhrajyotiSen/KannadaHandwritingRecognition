#### The paper describing this approach has been presented at 2018 3rd IEEE INTERNATIONAL CONFERENCE ON RECENT TRENDS ON ELECTRONICS, INFORMATION & COMMUNICATION TECHNOLOGY. 
Link to Publication - https://ieeexplore.ieee.org/document/9012531

## INSTALLATION

You need to have Python 3.x installed

`pip install -r requirements.txt`

The python libraries used are

```
scikit image
numpy
OpenCV
Django
Tensorflow
Joblib
Scipy
Matplotlib
Keras
Pillow
```
We also made use of a LRN2D layer which was removed from the keras source. It needs to be manually included.
-   Paste the contents of `keras_addition.txt` in `/usr/local/lib/python3.5/dist-packages/keras/layers/normalization.py`. 
-   Add `from .normalization import LRN2D` right under the import `from .normalization import BatchNormalization` in `/usr/local/lib/python3.5/dist-packages/keras/layers/__init__.py `. 
The file path may vary depending on your python version.
  
## KANNADA HANDWRITING RECOGNIZER

The project aims at Optical Character Recognition of handwritten documents in Kannada, a South Indian Language.

Kannada is being chosen as not much research was done prior with a whole document but only individual characters. The complexity further increases due to a very large number of classes due to letters, numbers, kagunitas and ottaksharas.

This project has also performed a comparative analysis of two supervised (k-Nearest neighbors and Support Vector Machines) and two unsupervised models (Inception V3 and Convoluted Neural Networks).

A web app provides the user interface. A handwritten document is given as input and the corresponding text as digital text is presented as an output in the web apps display

### DATASET

The dataset used is the Chars74K[http://www.ee.surrey.ac.uk/CVSSP/demos/chars74k/] dataset. It consists of a collection of images that belong to 657+ classes. Each class consists of 25 handwritten characters. Since a Deep Learning approach has also been used in this paper, the dataset needed to be expanded. This was done by using various augmentation techniques.

### PROPOSED APPROACH FOR KANNADA OCR

![](https://lh4.googleusercontent.com/4XyG2Tl-WNNUJYMD_s9sYxBajJYkqray6UP7rL9a2cYKoQm2F1n6U23QKMnYdEaqveAl5p5HsT_z6wENp63qyO9ROQqNXY908mQitX8CIgbtaFu42sl70ZYbPe_MEsvRcPpXAWMf)

### SEGMENTATION

The entire document is first segmented into lines, then words and at last into characters. Contour detection, Dilation and Bounded boxes method has been used for same.


### Ottakshara segmentation -

From the character obtained during character segmentation, we separate Ottakshara by considering its position along y axis with respect to the total height of the image.

Experimentations proved that all the contours that lie in the lower of the images could be considered as Ottakshara. The ottakshara identified is then mapped to the base character based on its position along x axis.

![](https://lh3.googleusercontent.com/u0sUSXn6Cn6jHld_D32P-01qEomqk8Yid5nT4CNHDeBpRMVhua_dLjFLJsrztdywN05AvGjKE6npY2RbCAL9cBlKPvbUmU9nOfN8GhOJPTY0BcdK0aq7cyOqvgBWqGY5sSNcqxBH)

### PREPROCESSING

The preprocessing steps that we carried out on our input images were - Grayscale, Noise Removal, Contrast Normalisation and Binarization.

![](https://lh5.googleusercontent.com/iLnVNrrp-dCNDu10glCeM-Me9So2JNtazPhAyDJihYS8jhlyx8BQYuJldK_EMl_HAr3DtcB7oG_tf38b-_NnJDotCxNZ48OKhpfC_3WL0wOVyvYyUdjAE0YdED0R5i_1W8SRxT3g)

### AUGMENTATION

Since certain models require large number of training data, it is practically not possible to write them. Due to this, we augmented the existing dataset to create more dataset for training phase. This has to be done with care so that overfitting does not happen.

The augmentation steps we considered were

-   Aspect ratio
    
-   Rotation
    
-   Smoothening
    
-   Padding
    
-   Noise
    
-   Resizing

![](https://lh4.googleusercontent.com/71bBj5oJ9LwygGo4ECZXlrQICDKZHqUE2zCyZ_744wtptWU2HROs8iVW8lOaOdj5m_LbVJ-gQziZ2ZVFiFKgzyJ0KqoQgUNwiclmfYFPhRebxRX3Sd8W3zNYvg-6mjZH1pFgias2)

Remove is also one of the augmentation steps we use. This is used to remove stray elements from the segmented character images. This is done by retaining the largest connected component. An example of how this step works is shown below

  

![](https://lh5.googleusercontent.com/jNZICq70K6w6sgYrc17XAm8RTnkfSrXCzGkN-zu-SqPu5C7CX5nHosgREVBHqN8GswSyLJpxR50lp_phCBxJkDqtnaPxrxIkatQVcZsWNULrzkJYBG7DUK4-ADwZ0gN7ZbmOqB3A)![](https://lh5.googleusercontent.com/xeNAQ0-1a36GuYdp5U2hcp8te8zozEaHJThcktsm10ADY_EUsWVaLmR0gyzrn5tpk_MfdHh2Xdh08ahblE9zQzE8YxWbhQwK8gO6zvVnKQ5fPp88nfwv1ZAaoUUy_oEOmVjHauLm)


### MNIST

MNIST like dataset was created from the augmented Chars74K dataset in order to train SVM and k-NN models.

### MODELS  AND VALUES OF PARAMETERS USED

#### Support Vector Machine

-   Histogram of Oriented Gradients were used as feature
    
-   Gamma - 0.001
    
-   C - 12.5
    
-   Kernel - Radial Basis function
    
#### k - Nearest Neighbours

-   Optimum k value - 5
    

#### Convolutional Neural Network

-   Alternating stacks of Convolutional layers followed by Max Pooling layers
    
-   Local Response Normalization layer is added to implement lateral inhibition.
    
-   Adam is chosen as the optimizer with a learning rate of 1e-2​
    
-   The learning rate was chosen using the method Cyclical Learning Rates for Training Neural Networks
    
-   Epoch - 100
    
-   Batch size - 100
    


Able to detect subtle variations in characters such as addition of kagunithas

  

#### Inception V3

-   Train percentage - 90%
    
-   Test percentage - 10%
    
-   Training Steps - 4000
    

### HOW TO EXECUTE

Check  ` web_app/hwrkannada\how_to_run.txt`


### RESULT

|Models |Accuracy |
|---|---|
| SVM| 96.35%|
| k-NN| 68.53%|
| CNN| 99.84%|
| Inception v3|75.36%|

### AUTHORS
- Subhrajyoti Sen
- Shreya V Prabhu
- Steve Jerold
- Pradeep JS
