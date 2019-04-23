import argparse
import sys
import numpy
np = numpy

def get_args_3t():
    def t_or_f(arg):
        ua = str(arg).upper()
        if 'TRUE'.startswith(ua):
            return True
        elif 'FALSE'.startswith(ua):
            return False
        else:
           raise ValueError('Arg is neither `True` nor `False`')

    def check_non_negative(value):
        ivalue = int(value)
        if ivalue < 0:
             raise argparse.ArgumentTypeError("%s is not non-negative!" % value)
        return ivalue

    def check_positive(value):
        ivalue = int(value)
        if ivalue < 1:
             raise argparse.ArgumentTypeError("%s is not positive!" % value)
        return ivalue

    def check_unit_interval(value):
        fvalue = float(value)
        if fvalue < 0 or fvalue > 1:
             raise argparse.ArgumentTypeError("%s is not in [0, 1] interval!" % value)
        return fvalue

    # No default value here. Indicate every single arguement.
    parser = argparse.ArgumentParser(
        description='three_tier.py\nNo default value! Indicate every argument.')

    # TODO: Fix the descriptions
    # Hyperparameter arguements:
    parser.add_argument('--exp', help='Experiment name',
            type=str, required=False, default='_')
    parser.add_argument('--seq_len', help='How many samples to include in each\
            Truncated BPTT pass', type=check_positive, required=True)
    parser.add_argument('--big_frame_size', help='How many samples per big frame',\
            type=check_positive, required=True)
    parser.add_argument('--frame_size', help='How many samples per frame',\
            type=check_positive, required=True)
    parser.add_argument('--weight_norm', help='Adding learnable weight normalization\
            to all the linear layers (except for the embedding layer)',\
            type=t_or_f, required=True)
    parser.add_argument('--emb_size', help='Size of embedding layer (> 0)',
            type=check_positive, required=True)  # different than two_tier
    parser.add_argument('--skip_conn', help='Add skip connections to RNN',
            type=t_or_f, required=True)
    parser.add_argument('--dim', help='Dimension of RNN and MLPs',\
            type=check_positive, required=True)
    parser.add_argument('--n_rnn', help='Number of layers in the stacked RNN',
            type=check_positive, choices=xrange(1,6), required=True)
    parser.add_argument('--rnn_type', help='GRU or LSTM', choices=['LSTM', 'GRU'],\
            required=True)
    parser.add_argument('--learn_h0', help='Whether to learn the initial state of RNN',\
            type=t_or_f, required=True)
    parser.add_argument('--q_levels', help='Number of bins for quantization of\
            audio samples. Should be 256 for mu-law.',\
            type=check_positive, required=True)
    parser.add_argument('--q_type', help='Quantization in linear-scale, a-law-companding,\
            or mu-law compandig. With mu-/a-law quantization level shoud be set as 256',\
            choices=['linear', 'a-law', 'mu-law'], required=True)
    parser.add_argument('--which_set', help='ONOM, BLIZZ, MUSIC, or HUCK, or SPEECH',
            choices=['ONOM', 'BLIZZ', 'MUSIC', 'HUCK', 'SPEECH', 'LESLEY','NANCY','VCBK'], required=True)
    parser.add_argument('--batch_size', help='size of mini-batch',type=check_positive, required=True)

    parser.add_argument('--debug', help='Debug mode', required=False, default=False, action='store_true')
    parser.add_argument('--resume', help='Resume the same model from the last\
            checkpoint. Order of params are important. [for now]',\
            required=False, default=False, action='store_true')
    
    parser.add_argument('--n_big_rnn', help='For tier3, Number of layers in the stacked RNN',\
            type=check_positive, choices=xrange(1,6), required=False, default=0)
    parser.add_argument('--frame_size_dnn', help='How many previous samples per setp for DNN',\
            type=check_positive, required=False, default=0)
    
    parser.add_argument('--rmzero', help='remove q_zero, start from real data',\
            required=False, default=False, action='store_true')
    parser.add_argument('--normed', help='normalize data on corpus level',\
            required=False, default=False, action='store_true')
    parser.add_argument('--utt', help='normalize data on utt level',\
            required=False, default=False, action='store_true')
    parser.add_argument('--grid', help='use data on air',\
            required=False, default=False, action='store_true')
    
    parser.add_argument('--quantlab', help='quantize labels',\
            required=False, default=False, action='store_true')
    
    parser.add_argument('--lr', help='learning rate',\
            type=float, required=False, default='0.001')
    
    parser.add_argument('--uc', help='uc starting point',
            type=str, required=False, default='flat_start')
    
    parser.add_argument('--acoustic', help='use acoustic features',required=False, default=False, action='store_true')
    parser.add_argument('--gen', help='pkl for strict synthesis',type=str, required=False, default='not_gen')
    
    parser.add_argument('--split', help='split data',required=False, default=False, action='store_true')
    parser.add_argument('--mol', help='use logistic mixture as output', type=check_positive, required=False, default=0)
    
    parser.add_argument('--t4tr', help='train with test set',required=False, default=False, action='store_true')
    parser.add_argument('--tr4t', help='test with train set 0',required=False, default=False, action='store_true')


    args = parser.parse_args()

    # NEW
    # Create tag for this experiment based on passed args
    tag_list = [t for t in sys.argv if ('--uc') not in t and '.pkl' not in t]
    tag = reduce(lambda a, b: a+b, tag_list).replace('--resume', '').replace('/', '-').replace('--', '-').replace('True', 'T').replace('False', 'F')
    #tag += '-lr'+str(LEARNING_RATE)
    print "Created experiment tag for these args:"
    print tag
    
    #deal with pb - dir name too long
    #option1
    #tag = reduce(lambda a, b: a+b, sys.argv[:-4]).replace('--resume', '').replace('/', '-').replace('--', '-').replace('True', 'T').replace('False', 'F')
    #option2
    tag = tag.replace('-which_setSPEECH','').replace('size','sz').replace('frame','fr').replace('batch','bch').replace('-grid', '')
    tag = tag.replace('-which_setLESLEY','').replace('-which_setNANCY','')

    return args, tag


def get_flag_dict(args):
    flag_dict = {}
    flag_dict['RMZERO'] = args.rmzero
    flag_dict['NORMED_ALRDY'] = args.normed
    flag_dict['NORMED_UTT'] = args.utt
    flag_dict['GRID'] = args.grid
    flag_dict['QUANTLAB'] = args.quantlab
    flag_dict['WHICH_SET'] = args.which_set
    flag_dict['ACOUSTIC'] = args.acoustic
    flag_dict['GEN'] = (args.gen!='not_gen')
    flag_dict['SPLIT'] = (args.split)
    flag_dict['MOL'] = (args.mol!=0)
    flag_dict['TR4T'] = args.tr4t
    return flag_dict

# ---------------------------------------------- for dataset.py
def get_file_lab_str(flag_dict,WHICH_SET):
    tmp_dict = {'SPEECH':'speech','LESLEY':'lesley','NANCY':'nancy','VCBK':'voicebank'}
    tmp_dataset = tmp_dict[WHICH_SET]
    tmp_norm = '_norm' if flag_dict['NORMED_ALRDY'] else ''
    # if WHICH_SET=='VCBK': tmp_norm += '_split'
    if flag_dict['SPLIT']: tmp_norm += '_split'
    
    tmp_cdv = 'trj' if flag_dict['ACOUSTIC'] else 'lab'
    __speech_file = '{dataset}/npyData/wav/MA_8s{norm}/{PH}.npy'.format(dataset=tmp_dataset,norm=tmp_norm,PH='{}')
    __speech_file_lab = '{dataset}/npyData/{cdv}/MA_8s{norm}/{PH}_{cdv}.npy'.format(dataset=tmp_dataset,norm=tmp_norm,cdv=tmp_cdv,PH='{}')
    return __speech_file,__speech_file_lab


def get_px_mol(x,pi,mu,s):
    #input: x, a scalar; pi,mu,s, three vectors containing MOL paras
    #output: px, prob of x under MOL defined by pi,mu,s
    cdf_plus = T.nnet.sigmoid((x+0.5-mu)/s)
    cdf_min = T.nnet.sigmoid((x-0.5-mu)/s)
    if x==0: cdf_min = 0
    if x==nb_levels: cdf_plus = 1
    return T.dot(pi,(cdf_plus-cdf_min))
    
    
def get_coding_seq_mol(inp,nb_mol,nb_levels):
    #input: 2d mtx (nb_samples,3*nb_mol), each row includes MOL params for a sample
    #output: 2d mtx (nb_samples,nb_levels), each row includes probability for each quantization bin
    # assert inp.shape.eval()[1]==(3*nb_mol), 'last dim (%s) of inp should be 3*nb_mol (3*%s)'%(inp.shape()[1],nb_mol)
    out = np.zeros(inp.shape()[0],nb_levels)
    for i,params in enumerate(inp):
        pi = params[:nb_mol]
        mu = params[nb_mol:2*nb_mol]
        s = params[2*nb_mol:3*nb_mol]
        for j,x in enumerate(xrange(0,nb_levels)):
            out[i,j] = get_px_mol(x,pi,mu,s)
    return out