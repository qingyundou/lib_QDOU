import os,sys
import datetime

def log_script(dir_tgt):
    # make dir_tgt
    if not os.path.exists(dir_tgt): os.makedirs(dir_tgt)
        
    # write info to LOG.txt
    with open(os.path.join(dir_tgt,'LOG.txt'),'w') as file_out:
        file_out.write(str(datetime.datetime.now()) + '\n')
        file_out.write('The following script is run:\n')
        file_out.write(os.path.abspath(sys.modules['__main__'].__file__) + '\n')
        file_out.write('Its content is:\n' + '-'*50 + '\n')
        with open(os.path.abspath(sys.modules['__main__'].__file__),'r') as file_in:
            data = file_in.read()
            file_out.write(data)
        file_out.write('\n' + '-'*50 + '\n')