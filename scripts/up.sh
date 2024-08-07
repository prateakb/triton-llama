set -e

MODEL_NAME="PY007/TinyLlama-1.1B-Chat-v0.3"
CLEANED_MODEL_NAME=${MODEL_NAME//\//_}
TRITON_MODEL_VERSION=1

echo "the hugging face model name is $CLEANED_MODEL_NAME"

echo "converting hugging face model to onnx format in $(PWD)/'outputs' folder"

python3 scripts/hugging_face_to_onnx.py $MODEL_NAME --output_folder "outputs"

echo "creating triton model repo"
mkdir -p models/tinyllama/$TRITON_MODEL_VERSION

cp outputs/$CLEANED_MODEL_NAME/* models/tinyllama/$TRITON_MODEL_VERSION/

echo "cleanup of staging onnx outputs"

rm -rf outputs
mkdir -p logs

echo "creating a virtual environment for testing the server"
python3 -m venv virtual_environment
source virtual_environment/bin/activate
python3 -m pip install -r requirements.txt

docker-compose up --build



