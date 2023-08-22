# Vision Language Models service

## Usage

### Install python packages:

* Prerequisites:

  * Python 3.10
  * Recommended: GPU with at least 16GB VRAM or 24GB VRAM for a better inference speed

* Install python packages:

  ```bash
  pip install -r requirements.txt
  ```

### Setup MiniGPT-4

1. Clone the project:

```bash
cd ./lib
git clone https://github.com/Vision-CAIR/MiniGPT-4.git
```

2. Follow [this section](https://github.com/Vision-CAIR/MiniGPT-4#installation), prepare weights of pretrained **Vicuna-7B** and **MiniGPT-4**
3. In `lib/MiniGPT-4/minigpt4/configs/models/minigpt4.yaml`, modify the `llama_model` with the path to **Vicuna-7B** weights
4. In `src/vqa/minigpt4_configs/minigpt4_eval.yaml`, modify the `model.ckpt` with the path to **MiniGPT4** weights

### Start service:

Prepare a `.env` file:

```bash
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=["*"]
CORS_HEADERS=["Content-Type","Authorization","X-Requested-With"]

# Settings for using S3 service
S3_BUCKET_NAME="<to be filled>"
AWS_ACCESS_KEY_ID="<to be filled>"
AWS_SECRET_ACCESS_KEY="<to be filled>"

# Model settings
DEVICE="cuda"
PREDICTOR_NAME="MiniGPT4"
PREDICTOR_ARGS="{'save_mem_mode': True}"
```

Start:

```bash
source ./scripts/start.sh
```

### Docker

```bash
docker build -t vqa-minigpt-4
```
