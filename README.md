# *Neural-Image-Colorization* using adversarial networks

<img src="" width="640px" align="right">

This is a Tensorflow implementation of *[Image-to-Image Translation with Conditional Adversarial Networks]()* that aims to infer a mapping from X to Y, where X is a single channel "black and white" image and Y is 3-channel "colorized" version of that image.

We make use of [Generative Adversarial Networks]() conditioned on the input to teach a generative neural network how to produce our desired results.

The purpose of this repository is to port the model over to TensorFlow.

## Results

<table style="width:100%">
  <tr>
    <th>Input</th> 
    <th>Output</th>
    <th>Ground-Truth</th>
  </tr>
  <tr>
    <td><img src="lib/readme_examples" width="100%"></td>
    <td><img src="lib/readme_examples" width=100%"></td> 
    <td><img src="lib/readme_examples" width=100%"></td> 
  </tr>
  <tr>
    <td><img src="lib/readme_examples" width="100%"></td>
    <td><img src="lib/readme_examples" width="100%"></td> 
    <td><img src="lib/readme_examples" width=100%"></td> 
  </tr>
  <tr>
    <td><img src="lib/readme_examples" width="100%"></td>
    <td><img src="lib/readme_examples" width="100%"></td> 
    <td><img src="lib/readme_examples" width=100%"></td> 
  </tr>
</table>

## Prerequisites

* [Python 3.5](https://www.python.org/downloads/release/python-350/)
* [TensorFlow](https://www.tensorflow.org/) (>= r1.0)
* [scikit-image](http://scikit-image.org/docs/dev/api/skimage.html)
* [NumPy](http://www.numpy.org/)

## Usage

To colorize a greyscale image using a trained model, invoke *colorize.py* and supply both the desired input image path and the saved model path.

```sh
python colorize.py 'path/to/input/image' 'path/to/saved/model'
```

To train a generative model to colorize images invoke *train.py* and supply a directory path containing a myriad of training examples. I suggest using a minimum of one million images. These images ough to be of the three-channel jpeg kind. Remember to check whether the images you have obtained are truly jpeg compressed. Often times creators of datasets will simply change the extensions of their images regardless of their types to ".jpg" without altering the actual data. 

```sh
python train.py 'path/to/training/dir'
```

## Files

* [colorize.py](./src/colorize.py)

    Main script that interprets the user's desired actions through parsed arguments. 
    
* [generator.py](./src/generator.py)
    
    Contains the generative net that can colorize single-channel images when trained.
    
* [discriminator.py](./src/discriminator.py)
    
    Contains the discriminative net that can discriminate between synthesized colorized images and ground-truth images.
    
* [net.py](./src/net.py)
    
    Contains the neural network super class with universal layer construction and instance normalization methods. 
    
* [train.py](./src/train.py)
    
    Contains a Trainer class that is responsible for training the generative adversarial networks and any related routines such as retrieving training data.