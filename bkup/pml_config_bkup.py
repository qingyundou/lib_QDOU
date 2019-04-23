import os, sys
sys.path.append('/home/dawna/tts/qd212/lib_QDOU/')
from CMD_bash import checkMakeDir

pml_src_path = '/home/dawna/tts/qd212/models/am_blstm/upcls_Nick_3xBLSTM1024_16kHz_LSE/percivaltts/external'
sys.path.append(pml_src_path)



# for 163D vocoder features, doesnt work with sigproc_pre201902
from pulsemodel.analysis import analysisf
def wav_2_ac(analysis_dir_in, analysis_dir_out, name):
    in_file_name = os.path.join(analysis_dir_in,'{}.wav'.format(name))
    if not os.path.isfile(in_file_name):
        in_file_name = os.path.join(analysis_dir_in,'{}.used.wav'.format(name))
    out_file_dict = {}
    out_file_dict['lf0'] = os.path.join(analysis_dir_out,'{}.lf0'.format(name))
    out_file_dict['mgc'] = os.path.join(analysis_dir_out,'{}.fwspec'.format(name))
    out_file_dict['bap'] = os.path.join(analysis_dir_out,'{}.fwnm'.format(name))
    
    analysisf(in_file_name, shift=0.005, dftlen=4096,
              finf0txt=None, f0_min=60, f0_max=600, ff0=out_file_dict['lf0'], f0_log=True, finf0bin=None,
              fspec=out_file_dict['mgc'], spec_mceporder=None, spec_fwceporder=None, spec_nbfwbnds=129,
              fpdd=None, pdd_mceporder=None, fnm=out_file_dict['bap'], nm_nbfwbnds=33, verbose=1)
    return

def wav_2_ac_list(analysis_dir_in, analysis_dir_out, name_list):
    checkMakeDir(analysis_dir_out)
    for name in name_list:
        wav_2_ac(analysis_dir_in, analysis_dir_out, name)
    return
        
        
# for 163D vocoder features, doesnt work with sigproc_pre201902
from pulsemodel.synthesis import synthesizef
def ac_2_wav(synthesis_dir_in, synthesis_dir_out, name):
    in_file_dict = {} 
    in_file_dict['lf0'] = os.path.join(synthesis_dir_in,'{}.lf0'.format(name))
    in_file_dict['mgc'] = os.path.join(synthesis_dir_in,'{}.fwspec'.format(name))
    in_file_dict['bap'] = os.path.join(synthesis_dir_in,'{}.fwnm'.format(name))
    out_file_name = os.path.join(synthesis_dir_out,'{}.wav'.format(name))

    synthesizef(16000, shift=0.005, dftlen=4096, 
        ff0=None, flf0=in_file_dict['lf0'], 
        fspec=None, ffwlspec=in_file_dict['mgc'], ffwcep=None, fmcep=None, 
        fnm=None, ffwnm=in_file_dict['bap'], nm_cont=False, fpdd=None, fmpdd=None, 
        fsyn=out_file_name, verbose=1)
    return

    
def ac_2_wav_list(synthesis_dir_in, synthesis_dir_out, name_list):
    checkMakeDir(synthesis_dir_out)
    for name in name_list:
        ac_2_wav(synthesis_dir_in, synthesis_dir_out, name)
    return