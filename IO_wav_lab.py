import numpy
np = numpy
import os
import scipy.io.wavfile
# import pdb
        

#20180228
def get_file_list(dirFile):
    f = open(dirFile,'r')
    tmp = f.readlines()
    fileList = [line[:-1] for line in tmp]
    f.close()
    return fileList

def readWav(dirFile,rate=3.0518e-05,FLAG_I2F=False):
    speech_wav = scipy.io.wavfile.read(dirFile)
    data = speech_wav[1]
    data = data.astype('float32')
    # if FLAG_I2F:
    if speech_wav[-1].dtype=='int16':
        #data *= rate
        data /= 32768.0
    return data

def readLab(dirFile):
    data = numpy.fromfile(dirFile, dtype='float32')
    data = data.reshape((data.shape[0]/601),601)
    return data

def load_binary_file(file_name, dimension):
    fid_lab = open(file_name, 'rb')
    features = numpy.fromfile(fid_lab, dtype=numpy.float32)
    fid_lab.close()
    # print file_name,features.size
    assert features.size % float(dimension) == 0.0,'specified dimension %s not compatible with data'%(dimension)
    features = features[:(dimension * (features.size / dimension))]
    features = features.reshape((-1, dimension))
    return  features

# def load_binary_file(file_name, dimension):
#     fid_lab = open(file_name, 'r')
#     features = numpy.fromfile(fid_lab, dtype=numpy.float32)
#     fid_lab.close()
#     # print file_name,features.size
#     assert features.size % float(dimension) == 0.0,'specified dimension %s not compatible with data'%(dimension)
#     features = features[:(dimension * (features.size / dimension))]
#     features = features.reshape((-1, dimension))
#     return  features

class   BinaryIOCollection(object):

    def load_binary_file(self, file_name, dimension):
        fid_lab = open(file_name, 'rb')
        features = numpy.fromfile(fid_lab, dtype=numpy.float32)
        fid_lab.close()
        assert features.size % float(dimension) == 0.0,'specified dimension %s not compatible with data'%(dimension)
        features = features[:(dimension * (features.size / dimension))]
        features = features.reshape((-1, dimension))
            
        return  features

    def array_to_binary_file(self, data, output_file_name):
        data = numpy.array(data, 'float32')
               
        fid = open(output_file_name, 'wb')
        data.tofile(fid)
        fid.close()

    def load_binary_file_frame(self, file_name, dimension):
        fid_lab = open(file_name, 'rb')
        features = numpy.fromfile(fid_lab, dtype=numpy.float32)
        fid_lab.close()
        assert features.size % float(dimension) == 0.0,'specified dimension %s not compatible with data'%(dimension)
        frame_number = features.size / dimension
        features = features[:(dimension * frame_number)]
        features = features.reshape((-1, dimension))
            
        return  features, frame_number

BITRATE = 16000
def write_audio_file(name, data, directory):
    data = data.astype('float32')
    data -= data.mean()
    scipy.io.wavfile.write(
                os.path.join(directory+name+'.wav'),
                BITRATE,
                data)
    return

BITRATE = 16000
def write_audio_file(name, data, save_dir):
        data = data.astype('float32')
#         data -= data.min()
#         data /= data.max()
#         data -= 0.5
#         data *= 0.95
        scipy.io.wavfile.write(
                    os.path.join(save_dir+name+'.wav'),
                    BITRATE,
                    data)

#---------------------------------------------------------

from sklearn import preprocessing

#option 1-1: normalize all to 0mean, 1var
def getNormedLabData(lab):
    rowNb,rowLen,featNb = lab.shape
    #1 reshape
    lab = lab.reshape(rowNb*rowLen,featNb)
#     print(lab.mean(axis=0)[:3])
#     print(lab.std(axis=0)[:3])
    #2 normalize
    lab = preprocessing.scale(lab)
#     print(lab.mean(axis=0)[:3])
#     print(lab.std(axis=0)[:3])
    #3 reshape back
    lab = lab.reshape(rowNb,rowLen,featNb)
    return lab
    
#option 1-2: fit normalizer on training data
def getNormedLabData_uni(lab,scaler):
    rowNb,rowLen,featNb = lab.shape
    #1 reshape
    lab = lab.reshape(rowNb*rowLen,featNb)
    #2 normalize
    lab = scaler.transform(lab)
    #3 reshape back
    lab = lab.reshape(rowNb,rowLen,featNb)
    return lab

#option 2-1: normalize all to 0~1, like in sampleRNN paper
def getMappedLabData(lab,feature_range=(0,1), copy=True):
    rowNb,rowLen,featNb = lab.shape
    lab = lab.reshape(rowNb*rowLen,featNb)
    min_max_scaler = preprocessing.MinMaxScaler()
    lab = min_max_scaler.fit_transform(lab)
    lab = lab.reshape(rowNb,rowLen,featNb)
    return lab

#option 2-2: fit normalizer on training data
def getMappedLabData_uni(lab,min_max_scaler,feature_range=(0,1), copy=True):
    rowNb,rowLen,featNb = lab.shape
    lab = lab.reshape(rowNb*rowLen,featNb)
    lab = min_max_scaler.transform(lab)
    lab = lab.reshape(rowNb,rowLen,featNb)
    return lab


#---------------------------------------------------------
#pre 2018
def printItemShape(d):
    for k,v in d.items():
        print(k),
        print(v.shape)

def checkIfMoreWav(wavs,labs,wav_fr=16000,lab_fr=200):
    cnt = 0
    cntPb = 0
    for wav,lab in zip(wavs,labs):
        cnt += 1
        alignLen = lab.shape[0]*(wav_fr/lab_fr) # 80
        if wav.shape[0]<alignLen:
            cntPb += 1
            print('wav less than lab*80')
            print(cnt)
            print(wav.shape[0],alignLen)
    if cntPb==0:
        print('all is well, wav>lab')
    return

def concatAll(wavs,labs,wav_fr=16000,lab_fr=200):
    #input: list, speech_{}_utt.npy, speech_{}_utt_lab/traj.npy
    #output: array, wav_all_array,lab_all_array
    wav_all_array = np.array([])
    lab_all_array = np.array([])

    for wav,lab in zip(wavs,labs):
        alignLen = lab.shape[0]*(wav_fr/lab_fr) # 80
        #wav_all_array = np.concatenate((wav_all_array,wav[-alignLen:]))
        wav_all_array = np.concatenate((wav_all_array,wav[:alignLen]))
        if len(lab_all_array)==0:
            lab_all_array = lab
        else:
            lab_all_array = np.concatenate((lab_all_array,lab))
    
    return wav_all_array,lab_all_array

def concatAll_fast(wavs,labs,wav_fr=16000,lab_fr=200):
    #input: list, speech_{}_utt.npy, speech_{}_utt_lab/traj.npy
    #output: array, wav_all_array,lab_all_array
    wavs = [w[:len(l)*(wav_fr/lab_fr)] for w,l in zip(wavs,labs)] # (wav_fr/lab_fr) = 80
    wav_all_array = np.concatenate(wavs, axis=0)
    lab_all_array = np.concatenate(labs, axis=0)
    return wav_all_array,lab_all_array

def cutEqLen(wav_all_array,lab_all_array,lab_dim=601,nb_sec=8,wav_fr=16000,lab_fr=200):
    # nb_sec = 8
    # cut ending, reshape into 8-sec rows
    allLen = len(wav_all_array)
    rowLen = nb_sec*wav_fr # 16000
    rowNb = allLen//rowLen
    wav_all_array_save = wav_all_array[:rowNb*rowLen].reshape(rowNb,rowLen)
    print('wav_all_array_save.shape:'),
    print(wav_all_array_save.shape)
    
    # cut ending, reshape into 8-sec rows
    allLen = len(lab_all_array)
    rowLen = nb_sec*lab_fr # 16000/80
    rowNb = allLen//rowLen
    lab_all_array_save = lab_all_array[:rowNb*rowLen].reshape(rowNb,rowLen,lab_dim)
    print('lab_all_array_save.shape:'),
    print(lab_all_array_save.shape)

    return wav_all_array_save,lab_all_array_save

def norm_utt(wav_utt):
    wav_utt_norm = wav_utt
    for utt in wav_utt_norm:
        utt -= utt.mean() #[-1,1], zero mean
        utt /= abs(utt).max()
        utt /= 2
        utt += 0.5 #[0,1],0.5 mean as if zero mean
    return wav_utt_norm

def rmDC_utt(wav_utt):
    wav_utt_norm = wav_utt
    for utt in wav_utt_norm:
        utt -= utt.mean() #[-1,1], zero mean
    return wav_utt_norm
