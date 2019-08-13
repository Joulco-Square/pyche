DIR_BASE="/usr/lib/python";
DIR=$DIR_BASE$1"/";

SCRIPT_DIR="$(realpath "$(dirname "$BASH_SOURCE")")"

if [ -d "$DIR" ]; then
  ### Take action if $DIR exists ###  
  ln -sf  $SCRIPT_DIR/../python_libraries/python$1/pyche  ${DIR};
  echo "Installing library files for Python version ${1}";
else
  ###  Control will jump here if $DIR does NOT exists ###
  echo "Python version ${1} not found. Skipping.";
  exit 1
fi