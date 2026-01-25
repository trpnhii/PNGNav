# Dockerfile for PNGNav ROS2 Gazebo Simulation
# Based on ROS2 Humble (Ubuntu 22.04)

FROM osrf/ros:humble-desktop-full

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV TURTLEBOT3_MODEL=waffle_pi
ENV ROS_DOMAIN_ID=0

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Build tools
    build-essential \
    cmake \
    git \
    wget \
    curl \
    vim \
    nano \
    # Python dependencies
    python3-pip \
    python3-venv \
    python3-dev \
    python3-numpy \
    # ROS2 dependencies
    ros-humble-turtlebot3* \
    ros-humble-turtlebot3-gazebo \
    ros-humble-turtlebot3-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-nav2-map-server \
    ros-humble-tf2-ros \
    ros-humble-tf2-tools \
    ros-humble-tf-transformations \
    ros-humble-rmw-cyclonedds-cpp \
    # Gazebo dependencies
    gazebo \
    libgazebo-dev \
    # Additional utilities
    x11-apps \
    xterm \
    # Cleanup
    && rm -rf /var/lib/apt/lists/*

# Install Python packages needed for ROS2 message generation (system Python)
# These must be in system Python, not conda, for colcon build to work
RUN pip3 install lark empy==3.3.4 catkin_pkg numpy

# Install Miniconda (but do NOT add to PATH globally - only in bashrc for interactive use)
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    bash /tmp/miniconda.sh -b -p /opt/conda && \
    rm /tmp/miniconda.sh && \
    /opt/conda/bin/conda clean -ya

# Set working directory
WORKDIR /workspace

# Copy environment file
COPY environment.yml /workspace/environment.yml

# Initialize conda for bash
RUN /opt/conda/bin/conda init bash

# Accept Conda Terms of Service for required channels
RUN /opt/conda/bin/conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main && \
    /opt/conda/bin/conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

# Create a minimal conda environment with Python 3.10 to match ROS2 Humble
RUN /opt/conda/bin/conda create -n pngenv python=3.10 pip setuptools wheel -y

# Install pip packages in conda environment
RUN /opt/conda/envs/pngenv/bin/pip install --no-cache-dir \
    addict==2.4.0 \
    ansi2html==1.8.0 \
    asttokens==2.2.1 \
    attrs==23.1.0 \
    backcall==0.2.0 \
    catkin-pkg==0.5.2 \
    certifi==2023.5.7 \
    charset-normalizer==3.1.0 \
    click==8.1.3 \
    cmake==3.26.4 \
    comm==0.1.3 \
    configargparse==1.5.5 \
    contourpy==1.1.0 \
    cycler==0.11.0 \
    dash==2.11.1 \
    dash-core-components==2.0.0 \
    dash-html-components==2.0.0 \
    dash-table==5.0.0 \
    debugpy==1.6.7 \
    decorator==5.1.1 \
    distro==1.8.0 \
    docutils==0.20.1 \
    empy==3.3.4 \
    executing==1.2.0 \
    fastjsonschema==2.17.1 \
    filelock==3.12.2 \
    flask==2.2.5 \
    fonttools==4.40.0 \
    idna==3.4 \
    importlib-metadata==6.7.0 \
    importlib-resources==5.12.0 \
    ipykernel==6.23.3 \
    ipython==8.14.0 \
    ipywidgets==8.0.6 \
    itsdangerous==2.1.2 \
    jedi==0.18.2 \
    jinja2==3.1.2 \
    joblib==1.3.1 \
    jsonschema==4.17.3 \
    jupyter-client==8.3.0 \
    jupyter-core==5.3.1 \
    jupyterlab-widgets==3.0.7 \
    kiwisolver==1.4.4 \
    lit==16.0.6 \
    markupsafe==2.1.3 \
    matplotlib==3.7.1 \
    matplotlib-inline==0.1.6 \
    mpmath==1.3.0 \
    multipledispatch==1.0.0 \
    nbformat==5.7.0 \
    nest-asyncio==1.5.6 \
    networkx==3.1 \
    numpy==1.25.0 \
    open3d==0.17.0 \
    opencv-python==4.8.0.74 \
    packaging==23.1 \
    pandas==2.0.3 \
    parso==0.8.3 \
    pexpect==4.8.0 \
    pickleshare==0.7.5 \
    pillow==10.0.0 \
    platformdirs==3.8.0 \
    plotly==5.15.0 \
    prompt-toolkit==3.0.38 \
    psutil==5.9.5 \
    ptyprocess==0.7.0 \
    pure-eval==0.2.2 \
    pygments==2.15.1 \
    pyparsing==3.1.0 \
    pyquaternion==0.9.9 \
    pyrr==0.10.3 \
    pyrsistent==0.19.3 \
    python-dateutil==2.8.2 \
    pytz==2023.3 \
    pyyaml==6.0 \
    pyzmq==25.1.0 \
    requests==2.31.0 \
    retrying==1.3.4 \
    rospkg==1.5.0 \
    scikit-learn==1.3.0 \
    scipy==1.11.1 \
    six==1.16.0 \
    stack-data==0.6.2 \
    sympy==1.12 \
    tenacity==8.2.2 \
    threadpoolctl==3.1.0 \
    tornado==6.3.2 \
    tqdm==4.65.0 \
    traitlets==5.9.0 \
    transforms3d==0.4.1 \
    triton==2.0.0 \
    typing-extensions==4.7.0 \
    tzdata==2023.3 \
    urllib3==2.0.3 \
    wcwidth==0.2.6 \
    werkzeug==2.2.3 \
    widgetsnbextension==4.0.7 \
    zipp==3.15.0 \
    lxml

# Install PyTorch with CUDA support
RUN /opt/conda/envs/pngenv/bin/pip install --no-cache-dir \
    torch==2.0.1 torchvision==0.15.2 \
    --extra-index-url https://download.pytorch.org/whl/cu121 || \
    /opt/conda/envs/pngenv/bin/pip install --no-cache-dir \
    torch==2.0.1 torchvision==0.15.2

# Clean up conda
RUN /opt/conda/bin/conda clean -ya

# Copy the entire project
COPY . /workspace/PNGNav

# Set up workspace
WORKDIR /workspace/PNGNav

# Make scripts executable
RUN find src/png_navigation/scripts -name "*.py" -exec chmod +x {} \; && \
    find src/png_navigation/scripts_dynamic_obstacles -name "*.py" -exec chmod +x {} \;

# Update shebang lines in scripts to use conda python
RUN find src/png_navigation/scripts -name "*.py" -type f -exec sed -i '1s|^#!/.*|#!/opt/conda/envs/pngenv/bin/python|' {} \; && \
    find src/png_navigation/scripts_dynamic_obstacles -name "*.py" -type f -exec sed -i '1s|^#!/.*|#!/opt/conda/envs/pngenv/bin/python|' {} \;

# Build the ROS2 package (using system Python - conda is NOT in PATH here)
RUN . /opt/ros/humble/setup.sh && \
    rm -rf build/ install/ log/ && \
    colcon build --packages-select png_navigation

# Setup bashrc for interactive use
RUN echo "" >> ~/.bashrc && \
    echo "# ROS2 setup" >> ~/.bashrc && \
    echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc && \
    echo "source /workspace/PNGNav/install/setup.bash" >> ~/.bashrc && \
    echo "export TURTLEBOT3_MODEL=waffle_pi" >> ~/.bashrc && \
    echo "export GAZEBO_MODEL_PATH=\$GAZEBO_MODEL_PATH:/opt/ros/humble/share/turtlebot3_gazebo/models" >> ~/.bashrc && \
    echo "" >> ~/.bashrc && \
    echo "# Conda setup (adds conda to PATH)" >> ~/.bashrc && \
    echo "export PATH=/opt/conda/bin:\$PATH" >> ~/.bashrc && \
    echo "conda activate pngenv" >> ~/.bashrc

# Create entrypoint script
RUN printf '#!/bin/bash\n\
    set -e\n\
    source /opt/ros/humble/setup.bash\n\
    source /workspace/PNGNav/install/setup.bash 2>/dev/null || true\n\
    export TURTLEBOT3_MODEL=waffle_pi\n\
    export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/opt/ros/humble/share/turtlebot3_gazebo/models\n\
    export PATH=/opt/conda/bin:$PATH\n\
    eval "$(/opt/conda/bin/conda shell.bash hook)"\n\
    conda activate pngenv\n\
    cd /workspace/PNGNav\n\
    exec "$@"\n' > /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command
CMD ["/bin/bash"]
