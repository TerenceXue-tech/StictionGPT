# Project Title

This project provides the dataset, data processing code, and training and testing code for paper: "StictionGPT: Detecting Valve Stiction in Control Loops using Large Vision Language Model"

---

## 📌 Abstract

Stiction detection in control valves is a critical challenge in control loop performance assessment and fault diagnosis within the process industry. Existing stiction detection methods often require determining a threshold or rely on large number of data to train deep neural networks. However, they face challenges such as difficulty in threshold determination, poor transferability, and lack of interpretability. Recent advancements in large language models (LLMs) and large vision-language models (LVLMs) have opened new avenues for industrial fault diagnosis by leveraging their reasoning and multimodal understanding capabilities. We propose StictionGPT, an LVLM-based agent for valve stiction detection. To overcome traditional method's limitations, we  leverage LVLMs to mimic human decision-making, combining textual semantics with visual shape features to determine the presence of stiction.  First, we transform time-series data into images that contain shape features. These images are time-series plot, PV-OP plot, OP-ΔPV plot and CRD-PV plot. Then, we create a multimodal dataset based on the semantics of these shapes for image-text alignment. Next, we fine-tune Qwen2.5-VL and InternVL2.5-MPO using low-rank adaption (LoRA) to adapt the LVLMs to stiction detection task. Finally, we test the model on the ISDB benchmark and deploy it in a chemical plant. StictionGPT achieves the highest accuracy on the ISDB benchmark and demonstrates excellent performance on the plant data.

---

## ⚙️ Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/TerenceXue-tech/StictionGPT.git
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   conda create -n StictionGPT python=3.10
   conda activate StictionGPT
   pip install -r requirements.txt
   ```

---

## 📂 Dataset

- Description of the dataset used (e.g., source, format, size).
- Optionally, include instructions on how to download or prepare the dataset.

Example:

```bash
wget https://example.com/dataset.zip
unzip dataset.zip -d ./data/
```

Make sure your data directory is structured as follows:

```
data/
├── train/
├── val/
└── test/
```

---

## 🏋️‍♂️ Training

To train the model, run:

```bash
python train.py --config configs/config.yaml
```

You can customize training parameters in the `configs/config.yaml` file.

---

## 🔍 Inference

To run inference on a single image or batch:

```bash
python inference.py --input_path path/to/image_or_folder --checkpoint path/to/model.ckpt
```

The output predictions will be saved in `./results/`.

---

## 📈 Results

Optionally include your performance metrics (e.g., accuracy, F1 score) and example outputs here.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙋 Citation

If you use this work in your research, please cite it as follows:

```
@misc{yourproject2025,
  title={Your Project Title},
  author={Your Name},
  year={2025},
  howpublished={\url{https://github.com/yourusername/yourproject}},
  note={Version 1.0}
}
```
