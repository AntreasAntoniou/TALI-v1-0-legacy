
########################################################################################
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh -O $HOME/conda.sh; bash $HOME/conda.sh -bf -p $HOME/conda/

CONDA_DIR=$HOME/conda/

echo "export "CONDA_DIR=${CONDA_DIR}"" >> $HOME/.bashrc

source $CONDA_DIR/bin/activate
########################################################################################

conda create -n tali python=3.8 -y
conda activate tali

conda install -c conda-forge git-lfs -y
conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch-nightly -y
conda install opencv -y

########################################################################################
echo "export CODE_DIR=$HOME/target_codebase" >> $HOME/.bashrc
echo "export MOUNT_DIR=/mnt/disk/tali/" >> $HOME/.bashrc
echo "export EXPERIMENTS_DIR=/mnt/disk/tali/experiments/" >> $HOME/.bashrc
echo "export DATASET_DIR=/mnt/disk/tali/dataset/" >> $HOME/.bashrc
echo "export TOKENIZERS_PARALLELISM=false" >> $HOME/.bashrc
echo "export FFREPORT=file=ffreport.log:level=32" >> $HOME/.bashrc
echo 'export OPENCV_LOG_LEVEL="SILENT"' >> $HOME/.bashrc

echo "source $CONDA_DIR/bin/activate" >> $HOME/.bashrc
echo "conda activate tali" >> $HOME/.bashrc

source $HOME/.bashrc
########################################################################################
cd $HOME
git clone https://github.com/AntreasAntoniou/TALI-lightning-hydra.git $CODE_DIR
cd $CODE_DIR

pip install -r $CODE_DIR/requirements.txt
pip install -e $CODE_DIR

#cd $HOME
#git clone https://huggingface.co/openai/clip-vit-base-patch32

########################################################################################
conda install gh --channel conda-forge -y
apt install htop nvtop -y
conda install google-cloud-sdk bat micro -y