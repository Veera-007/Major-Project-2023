# Major Project 2023
## **Noninvasive detection of root feeding insects using deep learning**
### Introduction
Weed control is essential in agriculture as weed competes with crops for space, nutrients, water, light and hinders the growth of crop. Conventional methods of weed removing involves herbicide spraying and manual removing using sickle. Removal of weed process can be automated by using artificial intelligence.

### Objectives
- To design Fractal dimension analysis to provide a semi-quantitative estimate of stridulation activity caused by the white grubs.
- Acquiring the audio from the stridulation activity of the white grubs and creating data set out of it.
- To implement deep learning techniques using (DNN) Deep neural network based classification for automatic detection of audio sections with stridulations.
- To quantify the density of the white grubs and provide a suitable solution to eradicate the white grubs from the rootlets of plants
  
### Methodology
The pre-processing of audio is done using audacity . The stirudulation features are extracted using R. Used Spectrogram to analyze and extract information such as frequency of white grubs noise. The model serves as the spectrogram-based classifier for the input audio files.

### Flow Chart
![Flowchart](https://github.com/Veera-007/Major-Project-2023/blob/main/Flowchartnew.PNG)

### DNN - ALGORITHM
- Convolutional Layer 1 - Applies a convolution operation to
the input data.
- Convolutional Layer 2 - Applies another convolution
operation to the previous layer's output. Followed by a
ReLU activation function.
- Flattening Layer - Reshapes the output from the previous
layer into a 1-dimensional vector
- Output Layer: Adds a dense layer with a number of units
equal to the target classes (3)

### Conclusion
Based on the stridulations count it was possible to detect the density of grubs.Hence fractal dimension analysis is a semi-quantitative analysis shifted to DNN for the analysis. Spectrograms are the major differentiating feature for audio files. So Model is trained and tested with a spectrogram as the feature. The model is up to 85-90\% accurate. Based on the output of the model best-suited recommendations are given for the farmers
