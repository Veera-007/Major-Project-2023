import keras
import os
import cv2
import sys
import random
import numpy as np
import ntpath
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import sounddevice as sd
import wavio as wv

from glob import glob
from tqdm import tqdm
from scipy.io.wavfile import write
from numpy.lib import stride_tricks
from matplotlib import pyplot as plt
from tkinter import filedialog
from PIL import ImageFile 
from keras.utils import np_utils
from tensorflow.keras.layers import Input, Convolution2D, Conv2DTranspose, Conv2D
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.callbacks import LearningRateScheduler
from tensorflow.keras import backend as K
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing import image 

# short-time Fourier Transformation(STFT)
def stft(sig, frame_size, overlap_factor=0.5, window=np.hanning):
    win = window(frame_size)
    hop_size = int(frame_size - np.floor(overlap_factor * frame_size))

    # zeros at beginning (thus center of 1st window should be for sample nr. 0)   
    samples = np.append(np.zeros(int(np.floor(frame_size / 2.0))), sig)
    # cols for windowing
    cols = np.ceil((len(samples) - frame_size) / float(hop_size)) + 1
    # zeros at end (thus samples can be fully covered by frames)
    samples = np.append(samples, np.zeros(frame_size))

    frames = stride_tricks.as_strided(samples, shape=(int(cols), frame_size), strides=(samples.strides[0] * hop_size, samples.strides[0])).copy()
    frames *= win

    return np.fft.rfft(frames)    

def log_scale_spec(spec, sr=44100, factor=20.):
    time_bins, frequency_bins = np.shape(spec)

    scale = np.linspace(0, 1, frequency_bins) ** factor
    scale *= (frequency_bins-1)/max(scale)
    scale = np.unique(np.round(scale))

    # Creates spectrogram with new frequency bins
    new_spectrogram = np.complex128(np.zeros([time_bins, len(scale)]))
    for i in range(0, len(scale)):        
        if i == len(scale)-1:
            new_spectrogram[:,i] = np.sum(spec[:,int(scale[i]):], axis=1)
        else:        
            new_spectrogram[:,i] = np.sum(spec[:,int(scale[i]):int(scale[i+1])], axis=1)

    # Lists center frequency of bins
    all_frequencies = np.abs(np.fft.fftfreq(frequency_bins*2, 1./sr)[:frequency_bins+1])
    frequemcies = []
    for i in range(0, len(scale)):
        if i == len(scale)-1:
            frequemcies += [np.mean(all_frequencies[int(scale[i]):])]
        else:
            frequemcies += [np.mean(all_frequencies[int(scale[i]):int(scale[i+1])])]

    return new_spectrogram, frequemcies

def plot_audio_spectrogram(audio_path, binsize=2**10, plot_path=None, argv = '', colormap="jet"):
    sample_rate, samples = wav.read(audio_path)
    samples=samples[1:1000000]
    s = stft(samples, binsize)
    new_spectrogram, freq = log_scale_spec(s, factor=1.0, sr=sample_rate)
    data = 20. * np.log10(np.abs(new_spectrogram) / 10e+6)  #dBFS

    time_bins, freq_bins = np.shape(data)

    print("Time bins: ", time_bins)
    print("Frequency bins: ", freq_bins)
    print("Sample rate: ", sample_rate)
    print("Samples: ",len(samples))
    # horizontal resolution correlated with audio length  (samples / sample length = audio length in seconds). If you use this(I've no idea why). I highly recommend to use "gaussian" interpolation.
    plt.figure(figsize=(time_bins/100, freq_bins/100)) # resolution equal to audio data resolution, dpi=100 as default
    plt.imshow(np.transpose(data), origin="lower", aspect="auto", cmap=colormap, interpolation="none")

    # Labels
    plt.xlabel("Time(s)")
    plt.ylabel("Frequency(Hz)")
    plt.xlim([0, time_bins-1])
    plt.ylim([0, freq_bins])


    if 'l' in argv: # Add Labels
        plt.colorbar().ax.set_xlabel('dBFS')
    else: # No Labels
        plt.subplots_adjust(left=0,right=1,bottom=0,top=1)
        plt.axis('off')

    x_locations = np.float32(np.linspace(0, time_bins-1, 10))
    plt.xticks(x_locations, ["%.02f" % l for l in ((x_locations*len(samples)/time_bins)+(0.5*binsize))/sample_rate])
    y_locations = np.int16(np.round(np.linspace(0, freq_bins-1, 20)))
    plt.yticks(y_locations, ["%.02f" % freq[i] for i in y_locations])


    if 's' in argv: # Save
        print('Unlabeled output saved as.png')
        print(plot_path)
        plt.savefig(plot_path)
    else:
        print('Graphic interface...')
        plt.show()

    plt.clf()

    return data
    
def path_to_tensor(img_path, width=224, height=224):
    # loads RGB image as PIL.Image.Image type
    print(img_path)
    img = image.load_img(img_path, target_size=(width, height))
    # convert PIL.Image.Image type to 3D tensor with shape (width, heigth, 3)
    x = image.img_to_array(img)
    # convert 3D tensor to 4D tensor with shape (1, width, height, 3) and return 4D tensor
    return np.expand_dims(x, axis=0)

def paths_to_tensor(img_paths, width=224, height=224):
    list_of_tensors = [path_to_tensor(img_paths, width, height)]
    return np.vstack(list_of_tensors)

clas1 = [item[9:-1] for item in sorted(glob("./output/*/"))]

#vilization_and_show()                    
ImageFile.LOAD_TRUNCATED_IMAGES = True

filename = filedialog.askopenfilename(title='open')
ims = plot_audio_spectrogram(filename, 2**10, ntpath.basename(filename.replace('.wav','')) + '.png',  's')
filename=ntpath.basename(filename.replace('.wav','')) + '.png'

img = cv2.imread(filename )
img=cv2.resize(img,(512,512))
plt.imshow(img)
plt.show()
bins = 8

# Prediction
model = load_model('trained_model_DNN1.h5')

test_tensors = paths_to_tensor(filename)/255
pred=model.predict(test_tensors)
print(np.argmax(pred))
print('Given Audio Predicted is : '+str(clas1[np.argmax(pred)]))
