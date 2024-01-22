
#assuming inside the productions directory

export ARCUBE_PRODUCTION_NAME="PicoRun4.1_1E17_RHC"
export ARCUBE_DIR="/home/fathimamaha/2x2_production/data/2x2_sim"
export PRODUCTION_HOST="fathimamaha@polaris.alcf.anl.gov"

mkdir $ARCUBE_PRODUCTION_NAME
cd $ARCUBE_PRODUCTION_NAME

scp -r $PRODUCTION_HOST:$ARCUBE_DIR/run-convert2h5/output/$ARCUBE_PRODUCTION_NAME.convert2h5 .
scp -r $PRODUCTION_HOST:$ARCUBE_DIR/run-edep-sim/output/$ARCUBE_PRODUCTION_NAME.nu .
scp -r $PRODUCTION_HOST:$ARCUBE_DIR/run-edep-sim/output/$ARCUBE_PRODUCTION_NAME.rock .
scp -r $PRODUCTION_HOST:$ARCUBE_DIR/run-larnd-sim/output/$ARCUBE_PRODUCTION_NAME.larnd .
scp -r $PRODUCTION_HOST:$ARCUBE_DIR/run-ndlar-flow/output/$ARCUBE_PRODUCTION_NAME.flow .
scp -r $PRODUCTION_HOST:$ARCUBE_DIR/validation/output/$ARCUBE_PRODUCTION_NAME.plots .
scp -r $PRODUCTION_HOST:$ARCUBE_DIR/run-spill-build/output/$ARCUBE_PRODUCTION_NAME.spill .




