from diffusers import StableDiffusionPipeline
import torch

# Load the pipeline
pipeline = StableDiffusionPipeline.from_pretrained(
    pretrained_model_name_or_path = 'runwayml/stable-diffusion-v1-5',
    torch_dtype = torch.float16,
    cache_dir = 'E:/AI/StableDiffusion/data/',
    safety_checker = None,
    low_cpu_mem_usage = True
)

pipeline.enable_attention_slicing()

# Move the pipeline to the GPU
pipeline.to("cuda")

# Prompt the pipeline
prompt = pipeline('tree')

# Save the generated image
prompt.images[0].save('E:/AI/test.png')
