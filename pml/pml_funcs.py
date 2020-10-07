### config parser
import pdb
def parse_pml_config_analysis(pml_config_analysis, analysis_dir_in, analysis_dir_out, name):
    in_file_name = os.path.join(analysis_dir_in,'{}.wav'.format(name))
    if not os.path.isfile(in_file_name):
        in_file_name = os.path.join(analysis_dir_in,'{}.used.wav'.format(name))
    out_file_dict = {}
    out_file_dict['lf0'] = os.path.join(analysis_dir_out,'{}.lf0'.format(name))
    out_file_dict['mgc'] = os.path.join(analysis_dir_out,'{}.fwspec'.format(name))
    out_file_dict['bap'] = os.path.join(analysis_dir_out,'{}.fwnm'.format(name))
    
    pml_config_analysis_out = dict(pml_config_analysis)
    for k,v in pml_config_analysis_out.items():
        if v=='{PH_fwav}': pml_config_analysis_out[k] = in_file_name
        elif v=='{PH_lf0}': pml_config_analysis_out[k] = out_file_dict['lf0']
        elif v=='{PH_mgc}': pml_config_analysis_out[k] = out_file_dict['mgc']
        elif v=='{PH_bap}': pml_config_analysis_out[k] = out_file_dict['bap']
            
    return pml_config_analysis_out

def parse_pml_config_synthesis(pml_config_synthesis, synthesis_dir_in, synthesis_dir_out, name):
    in_file_dict = {} 
    in_file_dict['lf0'] = os.path.join(synthesis_dir_in,'{}.lf0'.format(name))
    in_file_dict['mgc'] = os.path.join(synthesis_dir_in,'{}.fwspec'.format(name))
    in_file_dict['bap'] = os.path.join(synthesis_dir_in,'{}.fwnm'.format(name))
    out_file_name = os.path.join(synthesis_dir_out,'{}.wav'.format(name))
    
    pml_config_synthesis_out = dict(pml_config_synthesis)
    for k,v in pml_config_synthesis_out.items():
        if v=='{PH_fsyn}': pml_config_synthesis_out[k] = out_file_name
        elif v=='{PH_lf0}': pml_config_synthesis_out[k] = in_file_dict['lf0']
        elif v=='{PH_mgc}': pml_config_synthesis_out[k] = in_file_dict['mgc']
        elif v=='{PH_bap}': pml_config_synthesis_out[k] = in_file_dict['bap']
    
    return pml_config_synthesis_out


### PML wrapper
from __main__ import pml_config_analysis, pml_config_synthesis

import sys, os
sys.path.append('/home/dawna/tts/qd212/lib_QDOU/')
from CMD_bash import checkMakeDir

sys.path.append(pml_config_analysis['pml_src_path'])
from pulsemodel.analysis import analysisf

def wav_2_ac(analysis_dir_in, analysis_dir_out, name, pml_config_analysis=pml_config_analysis):
    cfg = parse_pml_config_analysis(pml_config_analysis, analysis_dir_in, analysis_dir_out, name)
    analysisf(cfg['fwav'], shift=cfg['shift'], dftlen=cfg['dftlen'],
              finf0txt=cfg['finf0txt'], f0_min=cfg['f0_min'], f0_max=cfg['f0_max'],
              ff0=cfg['ff0'], f0_log=cfg['f0_log'], finf0bin=cfg['finf0bin'],
              fspec=cfg['fspec'], spec_mceporder=cfg['spec_mceporder'], spec_fwceporder=cfg['spec_fwceporder'],
              spec_nbfwbnds=cfg['spec_nbfwbnds'],
              fpdd=cfg['fpdd'], pdd_mceporder=cfg['pdd_mceporder'], fnm=cfg['fnm'], nm_nbfwbnds=cfg['nm_nbfwbnds'], verbose=cfg['verbose'])
    return

def wav_2_ac_list(analysis_dir_in, analysis_dir_out, name_list):
    checkMakeDir(analysis_dir_out)
    for name in name_list:
        wav_2_ac(analysis_dir_in, analysis_dir_out, name)
    return

sys.path.append(pml_config_synthesis['pml_src_path'])
from pulsemodel.synthesis import synthesizef

def ac_2_wav(synthesis_dir_in, synthesis_dir_out, name, pml_config_synthesis=pml_config_synthesis):
    cfg = parse_pml_config_synthesis(pml_config_synthesis, synthesis_dir_in, synthesis_dir_out, name)
    synthesizef(cfg['fs'], shift=cfg['shift'], dftlen=cfg['dftlen'],
        ff0=cfg['ff0'], flf0=cfg['flf0'], 
        fspec=cfg['fspec'], ffwlspec=cfg['ffwlspec'], ffwcep=cfg['ffwcep'], fmcep=cfg['fmcep'], 
        fnm=cfg['fnm'], ffwnm=cfg['ffwnm'], nm_cont=cfg['nm_cont'], fpdd=cfg['fpdd'], fmpdd=cfg['fmpdd'], 
        fsyn=cfg['fsyn'], verbose=cfg['verbose'])
    return
    
def ac_2_wav_list(synthesis_dir_in, synthesis_dir_out, name_list):
    checkMakeDir(synthesis_dir_out)
    for name in name_list:
        ac_2_wav(synthesis_dir_in, synthesis_dir_out, name)
    return