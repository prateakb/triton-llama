import os
import argparse
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import onnxruntime
from onnxruntime.quantization import quantize_dynamic, QuantizationMode

def main(model_name, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Prepare model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16)

    # Prepare dummy inputs
    dummy_input = tokenizer("How to get in a good university?", return_tensors="pt").input_ids

    # Define ONNX file path
    model_safe_name = model_name.replace("/", "_")

    os.makedirs(os.path.join(output_folder, model_safe_name), exist_ok=True)

    onnx_file_path = os.path.join(output_folder, model_safe_name, "model.onnx")

    # Convert to ONNX using torch.onnx
    torch.onnx.export(
        model,
        (dummy_input,),
        onnx_file_path,
        opset_version=14,
        input_names=["input_ids"],
        output_names=["output"],
        dynamic_axes={"input_ids": {0: "batch_size", 1: "sequence_length"}, "output": {0: "batch_size", 1: "sequence_length"}},
        do_constant_folding=True
    )

    print(f"Model has been exported to {onnx_file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Hugging Face model to ONNX and quantize it.")
    parser.add_argument("model_name", type=str, help="Name of the model on Hugging Face")
    parser.add_argument("--output_folder", type=str, default="outputs", help="Folder to store the output files")
    args = parser.parse_args()

    main(args.model_name, args.output_folder)
