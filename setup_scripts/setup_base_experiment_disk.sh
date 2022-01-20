export MOUNT_DIR="/mnt/disk/filestore/"
export EXPERIMENTS_DIR="/mnt/disk/filestore/experiments/"

if [ ! -d "$MOUNT_DIR" ]; then
  mkdir -p $MOUNT_DIR
  chmod -Rv 777 $MOUNT_DIR
fi

if [ ! -d "$EXPERIMENTS_DIR" ]; then
  mkdir -p $EXPERIMENTS_DIR
  chmod -Rv 777 $EXPERIMENTS_DIR
fi
########################################################################################