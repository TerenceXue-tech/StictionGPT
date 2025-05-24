# StictionGPT: Detecting Valve Stiction in Process Control Loops using Large Vision Language Model
Authors: Tianci Xue, Chao Shang, Dexian Huang, Biao Huang

This project provides the dataset, data processing code, and training and testing code for [paper](https://dx.doi.org/10.2139/ssrn.5265092)

---

## 📌 Abstract

Stiction detection in control valves is a critical challenge in control loop performance assessment and fault diagnosis within the process industry. Existing stiction detection methods often require determining a threshold or rely on large number of data to train deep neural networks. However, they face challenges such as difficulty in threshold determination, poor transferability, and lack of interpretability. Recent advancements in large language models (LLMs) and large vision-language models (LVLMs) have opened new avenues for industrial fault diagnosis by leveraging their reasoning and multimodal understanding capabilities. We propose StictionGPT, an LVLM-based agent for valve stiction detection. To overcome traditional method's limitations, we  leverage LVLMs to mimic human decision-making, combining textual semantics with visual shape features to determine the presence of stiction.  First, we transform time-series data into images that contain shape features. These images are time-series plot, PV-OP plot, OP-ΔPV plot and CRD-PV plot. Then, we create a multimodal dataset based on the semantics of these shapes for image-text alignment. Next, we fine-tune Qwen2.5-VL and InternVL2.5-MPO using low-rank adaption (LoRA) to adapt the LVLMs to stiction detection task. Finally, we test the model on the ISDB benchmark and deploy it in a chemical plant. StictionGPT achieves the highest accuracy on the ISDB benchmark and demonstrates excellent performance on the plant data.

---

## ⚙️ Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/TerenceXue-tech/StictionGPT.git
   ```

2. Create a virtual environment and install dependencies for image construction:

   ```bash
   conda create -n StictionGPT python=3.10
   conda activate StictionGPT
   pip install -r requirements.txt
   ```

3. Install [ms-swift](https://github.com/modelscope/ms-swift) or [llama-factory](https://github.com/hiyouga/LLaMA-Factory) for SFT:

---

## 📂 Dataset

- [ISDB](https://sites.ualberta.ca/~bhuang/ISDB.zip), the benchmark for stiction detection task.
- Our plant dataset is available in this repository, and a detailed description can be found in our paper.

---

## 🧠 Foundation LVLM

Download Qwen2.5-VL-7B-Instruct and InternVL2.5-38B-MPO:

   ```bash
   git lfs install
   git clone https://www.modelscope.cn/Qwen/Qwen2.5-VL-7B-Instruct.git
   git clone https://www.modelscope.cn/OpenGVLab/InternVL2_5-38B-MPO.git
   ```

---



## 🏋️‍♂️ Training

Our devices: 8*RTX4090 GPUs. To fine-tuning the foundation model using ms-swift, run:

```python
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 NPROC_PER_NODE=8  nohup swift sft --torch_dtype 'bfloat16' --model '/home/shangchao/XTC/LLMs/InternVL2_5-38B-MPO' --model_type 'internvl2_5' --template 'internvl2_5' --dataset '/home/shangchao/XTC/LLaMA-Factory/data/stiction_loop.json' '/home/shangchao/XTC/LLaMA-Factory/data/stiction_loop_aug.json' '/home/shangchao/XTC/LLaMA-Factory/data/stiction_S_nonquantify2.json' '/home/shangchao/XTC/LLaMA-Factory/data/stiction_S_aug_nonquantify2.json' --max_length '1024' --init_weights 'True' --learning_rate '1e-4' --num_train_epochs '150.0' --attn_impl 'flash_attn' --gradient_accumulation_steps '8' --eval_steps '500' --output_dir 'output' --report_to 'tensorboard'  --deepspeed zero3  --add_version False --output_dir /home/shangchao/XTC/ms-swift/output/v14-20250311-104348 --logging_dir /home/shangchao/XTC/ms-swift/output/v14-20250311-104348/runs --ignore_args_error True > /home/shangchao/XTC/ms-swift/output/v14-20250311-104348/runs/run.log
```


---

## 🧱 Adapters

Download StictionGPT's LoRA adapter (our best checkpoint) at https://modelscope.cn/collections/StictionGPT-83e4ddfc50294e

---

## 🔍 Inference

To run inference on testing dataset:

```python
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 swift infer   --adapters /home/shangchao/XTC/ms-swift/output/internvl2.5-38B-t-best/checkpoint-200    --infer_backend pt    --temperature 0.5   --max_new_tokens 2048    --val_dataset /home/shangchao/XTC/plant_data/pre-stiction_t_plant_test.json   --max_batch_size 1 
```
---

📄 Citation

If you use this project or its results in your research, please cite:

```bibtex
@unpublished{xue2025stictiongpt,
  author    = {Xue, Tianci and Shang, Chao and Huang, Dexian and Huang, Biao},
  title     = {StictionGPT: Detecting Valve Stiction in Process Control Loops Using Large Vision Language Model},
  year      = {2025},
  url       = {https://dx.doi.org/10.2139/ssrn.5265092},
  doi       = {10.2139/ssrn.5265092}
}

```

---

