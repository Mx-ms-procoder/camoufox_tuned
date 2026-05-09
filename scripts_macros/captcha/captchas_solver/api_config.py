import os

# CapSolver API Key for ReCaptcha solving
CAPSOLVER_API_KEY = os.environ.get("CAPSOLVER_API_KEY", "")

# Nvidia API Keys for Vision Models
NVIDIA_API_KEY_Qwen = os.environ.get("NVIDIA_API_KEY_Qwen", os.environ.get("NVIDIA_API_KEY", ""))
NVIDIA_API_KEY_Gemma = os.environ.get("NVIDIA_API_KEY_Gemma", os.environ.get("NVIDIA_API_KEY", ""))
