### config
# PH means place holder, these are not really PML config, but data paths
pml_config_analysis = {
    'fwav':'{PH_fwav}',
    'shift':0.005, 'dftlen':4096,
    'finf0txt':None, 'f0_min':60, 'f0_max':600, 'ff0':'{PH_lf0}', 'f0_log':True, 'finf0bin':None,
    'fspec':'{PH_mgc}', 'spec_mceporder':None, 'spec_fwceporder':None, 'spec_nbfwbnds':129,
    'fpdd':None, 'pdd_mceporder':None, 'fnm':'{PH_bap}', 'nm_nbfwbnds':33, 'verbose':1,
    'pml_src_path':'/home/dawna/tts/qd212/models/am_blstm/upcls_Nick_3xBLSTM1024_16kHz_LSE/percivaltts/external'
}

pml_config_synthesis = {
    'fs':16000,
    'shift':0.005, 'dftlen':4096,
    'ff0':None, 'flf0':'{PH_lf0}',
    'fspec':None, 'ffwlspec':'{PH_mgc}', 'ffwcep':None, 'fmcep':None,
    'fnm':None, 'ffwnm':'{PH_bap}', 'nm_cont':False, 'fpdd':None, 'fmpdd':None,
    'fsyn':'{PH_fsyn}', 'verbose':1,
    'pml_src_path':'/home/dawna/tts/qd212/models/am_blstm/upcls_Nick_3xBLSTM1024_16kHz_LSE/percivaltts/external'
}









