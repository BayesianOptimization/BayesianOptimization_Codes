<!-- background: #e4dadf-->
<!-- color: #774c43 -->
<!-- font: univers -->

<h1 align="center">
<span style = "color: #FFC300">
BayesianOptimization_Codes
</span>
</h1>

* * *
## Introduction
 This repository consists of codes for Practical First Order Bayesian Optimization Algorithms.
***
## Installation
For installing the repository use the command below in your terminal.<br>
<code>
<blink>
    git clone https://github.com/BayesianOptimization/BayesianOptimization_Codes/    
</blink>
</code>
***
## Description
### src_RL:
This folder consists of all the Reinforcement Learning files and once run and properly set will give RL results.<br />
To run all RL experiments use command:
<code>
<blink>
    make all  
</blink>
</code>
This will start the experiments for RL.


**Libraries required to run the code include numpy,scikit,keras,Imageio and matplotlib which are thoroughly used all over the code.**

### Problem4&5:
In this part of the excercise we had to use our own sample RGB image and use the incomplete data to reconstruct the image and compare them.<br />
Steps to follow if you want to test on your own sample image.
* First follow the installation step to clone the repository.
* Now, use the problem4&5 folder to access code for testing on your own sample image.
The folder consists of:
  * create_random_indices.ipynb
  * combine_comp.ipynb
  * Get_corrupted.ipynb
  * Sample images
  * img.Png
  * R
  * G
  * B
* Select a 100X100 pixel image (otherwise PC might crash) and use create_random_indices.ipynb to select randomly some pixels which you want to retain in incomplete image.
* Folders R,G,B are used to do reconstruction separately for Red,Green and Blue components respectively.Each of them contains two files create_data.ipynb and recons.ipynb.
* One by one use create data for obtaining incomplete matrices to be used in recons.ipynb to reconstruct image.
* Firstly create data and then use recons for each R,G,B for obtaing reconstructed image of that particular component.
* Check the R,G,B folders once execution complete.If a new folder 'data for assignment' has been created and file with extension .npy is created then execution is successful.
* Now for the final step use comine_comp.ipynb to combine all components into one image and compare with the final image.
* Sample_images contains reconstructed images used as a reference:
  * reconstruct_0.4.png - reconstructed image when corruption 40%
  * reconstruct_0.7.png - reconstructed image when corruption 70%
* img.png is the sample image used for reconstruction.

**NOTE:Change path variable according to your files in order for the code to work properly.**
