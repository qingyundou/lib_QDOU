if [[ "$#" -gt 0 ]]
then
    export X_SGE_CUDA_DEVICE=$@
    echo "using gpu $X_SGE_CUDA_DEVICE"
else
    echo "X_SGE_CUDA_DEVICE is not set, not using gpu"
fi
# export CUDA_VISIBLE_DEVICES=$X_SGE_CUDA_DEVICE


# if [[ $HOSTNAME == *"air2"* ]]
# then
#     echo "on $HOSTNAME, device should be auto assigned"
# else
#     if [[ "$#" -gt 0 ]]
#     then
#         X_SGE_CUDA_DEVICE=$@
#     fi
#     echo "on $HOSTNAME, using device $X_SGE_CUDA_DEVICE"
# fi