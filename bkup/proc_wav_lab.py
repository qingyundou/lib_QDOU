import numpy
np = numpy
import os
import scipy.io.wavfile
# import pdb

import sys
sys.path.insert(0, '/home/dawna/tts/qd212/lib_QDOU')

from cmd import *
from IO_wav_lab import *

class Configuration:
    def __init__(self):
        self.work_dir = '/home/dawna/tts/qd212/mphilproj/data'
        self.data_dir = os.path.join(self.work_dir, 'speech')
        self.wav_dir = os.path.join(self.data_dir, 'speechRawWavData')
        self.lab_dir = os.path.join(self.data_dir, 'speechGenCmpData')
        # self.lab_dir = '/home/dawna/tts/gad27/exp/char2wav/upcls_Nick_3xBLSTM1024_16kHz_LSE/out/model-gen/' #alternative
        self.file_id_list = os.path.join(self.data_dir, 'file_id_list.scp')
        
        self.output_dir_wav = os.path.join(self.data_dir, 'speechNpyData/wav')
        self.output_dir_lab = os.path.join(self.data_dir, 'speechNpyData/lab')
        self.output_dir_wav_utt = os.path.join(self.output_dir_wav, 'utt')
        self.output_dir_lab_utt = os.path.join(self.output_dir_lab, 'utt_traj')
        
        self.lab_dim = 163
        
        self.file_dict = {}
        self.file_dict['train_file'] = {'start_file_index': 0, 'end_file_index': 2253, 'nb_repeat':0}
        self.file_dict['valid_file'] = {'start_file_index': 2254, 'end_file_index': 2323, 'nb_repeat':0}
        self.file_dict['test_file'] = {'start_file_index': 2324, 'end_file_index': 2395, 'nb_repeat':0}
        
        self.flag_mk_utt = True
        self.flag_norm_wav = False
        self.flag_mk_lab = False
        
        if self.flag_norm_wav == True:
            self.output_dir_wav_mtx = os.path.join(self.output_dir_wav,'MA_f32_8s_norm_utt')
            self.output_dir_lab_mtx = os.path.join(self.output_dir_lab,'MA_lab_8s_norm')
        else:
            self.output_dir_wav_mtx = os.path.join(self.output_dir_wav,'MA_f32_8s')
            self.output_dir_lab_mtx = os.path.join(self.output_dir_lab,'MA_lab_8s_norm')
        

#20180228
def mk_utt_files(fileList,cfg):
    # wav_dir = 'lesley/16k_resil_LesleySimsFixedPauses/'
    # lab_dir = '/home/dawna/tts/zm273/LesleySimsFixedPauses_baseline/data/nn_no_silence_lab_norm_601'
    output_dir_wav_utt = cfg.output_dir_wav_utt
    output_dir_lab_utt = cfg.output_dir_lab_utt
    checkMakeDir(output_dir_wav_utt)
    checkMakeDir(output_dir_lab_utt)
    
    speech_utt = []
    speech_utt_lab = []
    cnt = 0
    print 'making utt npy files'
    for f in fileList:
        cnt += 1
        print cnt,f
        wav = readWav(os.path.join(cfg.wav_dir,f+'.used.wav'))
        lab = load_cmp_file(os.path.join(cfg.lab_dir,f+'.cmp'),cfg.lab_dim)
        speech_utt.append(wav)
        speech_utt_lab.append(lab)
        
    speech_train_utt = speech_utt[cfg.file_dict['train_file']['start_file_index']:cfg.file_dict['train_file']['end_file_index']+1]
    speech_valid_utt = speech_utt[cfg.file_dict['valid_file']['start_file_index']:cfg.file_dict['valid_file']['end_file_index']+1]
    speech_test_utt = speech_utt[cfg.file_dict['test_file']['start_file_index']:cfg.file_dict['test_file']['end_file_index']+1]
    speech_train_utt_lab = speech_utt_lab[cfg.file_dict['train_file']['start_file_index']:cfg.file_dict['train_file']['end_file_index']+1]
    speech_valid_utt_lab = speech_utt_lab[cfg.file_dict['valid_file']['start_file_index']:cfg.file_dict['valid_file']['end_file_index']+1]
    speech_test_utt_lab = speech_utt_lab[cfg.file_dict['test_file']['start_file_index']:cfg.file_dict['test_file']['end_file_index']+1]

    # numpy.save(output_dir_wav_utt+'/speech_{}_utt.npy'.format('train'),speech_train_utt)
    # numpy.save(output_dir_wav_utt+'/speech_{}_utt.npy'.format('valid'),speech_valid_utt)
    # numpy.save(output_dir_wav_utt+'/speech_{}_utt.npy'.format('test'),speech_test_utt)
    # numpy.save(output_dir_lab_utt+'/speech_{}_utt_lab.npy'.format('train'),speech_train_utt_lab)
    # numpy.save(output_dir_lab_utt+'/speech_{}_utt_lab.npy'.format('valid'),speech_valid_utt_lab)
    # numpy.save(output_dir_lab_utt+'/speech_{}_utt_lab.npy'.format('test'),speech_test_utt_lab)
    numpy.save(output_dir_lab_utt+'/speech_{}_utt_traj.npy'.format('train'),speech_train_utt_lab)
    numpy.save(output_dir_lab_utt+'/speech_{}_utt_traj.npy'.format('valid'),speech_valid_utt_lab)
    numpy.save(output_dir_lab_utt+'/speech_{}_utt_traj.npy'.format('test'),speech_test_utt_lab)
    return


#pre 2018
def printItemShape(d):
    for k,v in d.items():
        print(k),
        print(v.shape)

def checkIfMoreWav(wavs,labs):
    cnt = 0
    cntPb = 0
    for wav,lab in zip(wavs,labs):
        cnt += 1
        alignLen = lab.shape[0]*80
        if wav.shape[0]<alignLen:
            cntPb += 1
            print('wav less than lab*80')
            print(cnt)
            print(wav.shape[0],alignLen)
    if cntPb==0:
        print('all is well, wav>lab')
    return

def concatAll(wavs,labs):   
    wav_all_array = np.array([])
    lab_all_array = np.array([])

    for wav,lab in zip(wavs,labs):
        alignLen = lab.shape[0]*80
        #wav_all_array = np.concatenate((wav_all_array,wav[-alignLen:]))
        wav_all_array = np.concatenate((wav_all_array,wav[:alignLen]))
        if len(lab_all_array)==0:
            lab_all_array = lab
        else:
            lab_all_array = np.concatenate((lab_all_array,lab))
    
    return wav_all_array,lab_all_array

def cutEqLen(wav_all_array,lab_all_array):
    nb_sec = 8
    # cut ending, reshape into 8-sec rows
    allLen = len(wav_all_array)
    rowLen = nb_sec*16000
    rowNb = allLen//rowLen
    wav_all_array_save = wav_all_array[:rowNb*rowLen].reshape(rowNb,rowLen)
    print('wav_all_array_save.shape:'),
    print(wav_all_array_save.shape)
    
    # cut ending, reshape into 8-sec rows
    allLen = len(lab_all_array)
    rowLen = nb_sec*16000/80
    rowNb = allLen//rowLen
    lab_all_array_save = lab_all_array[:rowNb*rowLen].reshape(rowNb,rowLen,601)
    print('lab_all_array_save.shape:'),
    print(lab_all_array_save.shape)

    return wav_all_array_save,lab_all_array_save


def mk_mtx_files(cfg, file_list):
    print('1 -------------- prepare utt & utt_lab')
    #wav
    output_dir_wav_utt = cfg.output_dir_wav_utt
    dirFile = os.path.join(output_dir_wav_utt,'speech_train_utt.npy')
    speech_train_utt = numpy.load(dirFile)
    dirFile = os.path.join(output_dir_wav_utt,'speech_valid_utt.npy')
    speech_valid_utt = numpy.load(dirFile)
    dirFile = os.path.join(output_dir_wav_utt,'speech_test_utt.npy')
    speech_test_utt = numpy.load(dirFile)

    #lab
    output_dir_lab_utt = cfg.output_dir_lab_utt
    dirFile = os.path.join(output_dir_lab_utt,'speech_train_utt_lab.npy')
    speech_train_utt_lab = numpy.load(dirFile)
    dirFile = os.path.join(output_dir_lab_utt,'speech_valid_utt_lab.npy')
    speech_valid_utt_lab = numpy.load(dirFile)
    dirFile = os.path.join(output_dir_lab_utt,'speech_test_utt_lab.npy')
    speech_test_utt_lab = numpy.load(dirFile)

    wavDict = {}
    wavDict['train'] = speech_train_utt
    wavDict['valid'] = speech_valid_utt
    wavDict['test'] = speech_test_utt
    labDict = {}
    labDict['train'] = speech_train_utt_lab
    labDict['valid'] = speech_valid_utt_lab
    labDict['test'] = speech_test_utt_lab

    printItemShape(wavDict)
    printItemShape(labDict)
    for k in wavDict:
        print(k+': '),
        checkIfMoreWav(wavDict[k],labDict[k])

    if cfg.flag_norm_wav == True:
        print('1.5 -------------- normalize on utt level: rm mean, increase volume')
        for k in wavDict:
            print(k+': '),
            for utt in wavDict[k]:
                utt -= utt.mean() #[-1,1], zero mean
                utt /= abs(utt).max()
                utt /= 2
                utt += 0.5 #[0,1],0.5 mean as if zero mean
            print 'ok'

    print('2 -------------- manually align utt & utt_lab, get wav_all_array_save & lab_all_array_save')
    wavSaveDict = {}
    labSaveDict = {}
    for k in wavDict:
        print(k+': ')
        wav_all_array,lab_all_array = concatAll(wavDict[k],labDict[k])
        if k in ['valid','test']:
            tmp_wav,tmp_lab = wav_all_array,lab_all_array
            nb_repeat = cfg.file_dict['{}_file'.format(k)]['nb_repeat']#should be 0 normally
            print('nb_repeat: '+str(nb_repeat))
            for i in range(nb_repeat):
                wav_all_array = np.concatenate((wav_all_array,tmp_wav))
                lab_all_array = np.concatenate((lab_all_array,tmp_lab))
        wav_all_array_save,lab_all_array_save = cutEqLen(wav_all_array,lab_all_array)
        wavSaveDict[k],labSaveDict[k] = wav_all_array_save,lab_all_array_save
        
    # pdb.set_trace()

    print('3 -------------- save wav_all_array_save & lab_all_array_save')
    tgt_dir_wav = cfg.tgt_dir_wav
    tgt_dir_lab = cfg.tgt_dir_lab
    checkMakeDir(tgt_dir_wav)
    checkMakeDir(tgt_dir_lab)

    for k in wavDict:
        print(k+': ')
        numpy.save(tgt_dir_wav+'/speech_{}.npy'.format(k),wavSaveDict[k])
        if cfg.flag_mk_lab == True:
            numpy.save(tgt_dir_lab+'/speech_{}_lab.npy'.format(k),labSaveDict[k])
    print('00 -------------- complete')

    
if __name__ == '__main__': 
    cfg = Configuration()
    file_list = get_file_list(cfg.file_id_list)
    if cfg.flag_mk_utt == True:
        mk_utt_files(file_list,cfg)
    # mk_mtx_files(cfg, file_list)
    
    

