#!/bin/bash

# This script automates the setup of the Conda environment for the
# Delivery Route Optimization project using a hybrid conda/pip approach.

ENV_NAME="delivery-optimization-service"
PYTHON_VERSION="3.10"

echo "================================================================="
echo "Creating Conda environment: $ENV_NAME with Python $PYTHON_VERSION"
echo "================================================================="
conda create --name $ENV_NAME python=$PYTHON_VERSION -y

# Activate the environment for the following commands using 'conda run'
# This is the recommended way to run commands in a conda env from a script.

echo "\n================================================================="
echo "Installing complex packages with Conda (Geospatial & PyTorch)..."
echo "================================================================="
# Install geospatial stack from conda-forge for stability
conda run -n $ENV_NAME conda install -c conda-forge osmnx geopandas -y

# Install PyTorch (CPU version) from the pytorch channel
conda run -n $ENV_NAME conda install -c pytorch pytorch torchvision torchaudio cpuonly -y

echo "\n================================================================="
echo "Installing remaining packages from requirements.txt using pip..."
echo "================================================================="
conda run -n $ENV_NAME pip install -r requirements.txt

echo "\n================================================================="
echo "Creating environment.yml file for full reproducibility..."
echo "================================================================="
conda env export --name $ENV_NAME --from-history > environment.yml
echo "NOTE: An 'environment.yml' file has been created. You can use it to"
echo "recreate this exact environment with: conda env create -f environment.yml"


echo "\n================================================================="
echo "Setup complete!"
echo "To activate the environment, run: conda activate $ENV_NAME"
echo "================================================================="