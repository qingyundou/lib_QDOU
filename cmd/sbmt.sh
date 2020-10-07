SCRIPT=${1:-none}
MACHINE=${2:-anyair}
NGPUS=${3:-1}

SLEEP_DIR=/home/dawna/tts/qd212/lib_QDOU/sleep
SLEEP=${SLEEP_DIR}/multi_sl.sh

if [[ "$SCRIPT" == none ]] || [[ "$MACHINE" != *"air"* ]]; then
    echo "Usage: $0 script machine ngpus"
    echo "  e.g: $0 run.sh air204 2"
    echo "  got: $0 $@"
    exit 100
fi

echo SCRIPT $SCRIPT
echo MACHINE $MACHINE
echo NGPUS $NGPUS


if [ $MACHINE == anyair ]; then
    MACHINE='*'
    # echo "$MACHINE"
fi

if [ $NGPUS -eq 0 ]; then
    queue_priority=low
else
    queue_priority=cuda-low
fi


export TMP=$(date '+%Y%m%d-%H:%M:%S').txt
echo "$TMP" > /home/dawna/tts/qd212/lib_QDOU/sleep/temp/${TMP}

# cmd="qsub -M qd212@cam.ac.uk -m bea -S /bin/bash -l queue_priority=${queue_priority},tests=0,mem_grab=0M,gpuclass=*,osrel=*,hostname=$MACHINE $(pwd)/${SCRIPT}"
# echo $cmd
qsub -M qd212@cam.ac.uk -m bea -S /bin/bash -l queue_priority=${queue_priority},tests=0,mem_grab=0M,gpuclass=*,osrel=*,hostname=$MACHINE $(pwd)/${SCRIPT} ${TMP}

i=1
while [ $i -lt $NGPUS ]; do
#     echo sleep$i
    qsub -M qd212@cam.ac.uk -m bea -S /bin/bash -l queue_priority=cuda-low,tests=0,mem_grab=0M,gpuclass=*,osrel=*,hostname=$MACHINE $SLEEP ${TMP}
    i=$[$i+1]
done