
# Imports
import os
import requests
import json
import uuid

import pandas as pd
import numpy as np
import time


def image_summarizer(uploaded_file):
    vila_prompt = """
    Analyze this image and provide a detailed summary focusing on elements relevant to incident assessment and response. The summary should include:
    Scene Description & Environment: Describe the overall environment (e.g., urban, rural, industrial, natural landscape), the visible terrain, and any significant features like structures, vehicles, or natural elements. Note the time of day or lighting conditions.
    Incident Characteristics: Identify the type of incident (e.g., accident, hazard, natural disaster, security event). Describe its apparent scale, severity, and any visible progression or impact.
    Visible Entities & Activities: List any people, vehicles, equipment, or other relevant objects present in the image. Describe their roles or activities, if discernible (e.g., responders, victims, bystanders, operational tasks).
    Hazards, Risks & Damage: Detail any immediate or potential hazards (e.g., smoke, debris, spills, instability, exposed elements) and any visible damage to property, infrastructure, or the environment.
    Contextual Clues: Point out any signs, markings, or other visual cues that provide additional context about the incident (e.g., license plates, company logos, warning signs, weather indicators).
    Inferred Urgency & Priority: Based on the visual evidence, infer the immediate urgency of the situation and suggest potential priorities for response (e.g., life safety, containment, damage control).
    Key Elements (Concise List): Provide a brief, bulleted list of the most critical elements identified that define the situation.
    The summary should be objective, descriptive, and focus on providing concrete observations that would inform a rapid response or further investigation.
    Also generate the probablity/confidence of threat.
    Give the answer in json format, no extra information.

    NUMERIC FORMAT ‒ Probabilities must be written with **two decimals** (e.g. 0.03, 0.58, 0.97).   ‒ Avoid rounding everything to extremes like 0.00 or 1.00 unless highly certain.
    Keep image summary under 200 words.
    **OUTPUT/JSON FORMAT**:
    {
        "image_summary":[summary of image]
        "probablity":[probablity/confidence of the threat]
    } 
    """
    
    media_samples = [uploaded_file]

    invoke_url = "https://ai.api.nvidia.com/v1/vlm/nvidia/vila"
    stream = False
    kApiKey = os.getenv("NVIDIA_API_KEY")
    assert kApiKey, "Please set API_KEY"

    kNvcfAssetUrl = "https://api.nvcf.nvidia.com/v2/nvcf/assets"
    kSupportedList = {
        "png": ["image/png", "img"],
        "jpg": ["image/jpg", "img"],
        "jpeg": ["image/jpeg", "img"],
        "mp4": ["video/mp4", "video"],
    }
    
    def get_extention(filename):
        _, ext = os.path.splitext(filename)
        return ext[1:].lower()

    def mime_type(ext):
        return kSupportedList[ext][0]

    def media_type(ext):
        return kSupportedList[ext][1]

    def _upload_asset(media_file, description):
        ext = get_extention(media_file)
        assert ext in kSupportedList, f"Unsupported file format: {ext}"
        data_input = open(media_file, "rb")
        headers = {
            "Authorization": f"Bearer {kApiKey}",
            "Content-Type": "application/json",
            "accept": "application/json",
        }
        authorize = requests.post(
            kNvcfAssetUrl,
            headers=headers,
            json={"contentType": mime_type(ext), "description": description},
            timeout=30,
        )
        authorize.raise_for_status()
        authorize_res = authorize.json()
        print(f"Uploading to: {authorize_res['uploadUrl']}")
        response = requests.put(
            authorize_res["uploadUrl"],
            data=data_input,
            headers={
                "x-amz-meta-nvcf-asset-description": description,
                "content-type": mime_type(ext),
            },
            timeout=300,
        )
        response.raise_for_status()
        print(f"Uploaded asset_id {authorize_res['assetId']}")
        return uuid.UUID(authorize_res["assetId"])

    def _delete_asset(asset_id):
        headers = {
            "Authorization": f"Bearer {kApiKey}",
        }
        delete_url = f"{kNvcfAssetUrl}/{asset_id}"
        response = requests.delete(delete_url, headers=headers, timeout=30)
        response.raise_for_status()

    def chat_with_media_nvcf(infer_url, media_files, query: str, stream: bool = False):
        asset_list = []
        media_content = ""
        has_video = False

        for media_file in media_files:
            ext = get_extention(media_file)
            assert ext in kSupportedList, f"{media_file} format is not supported"
            if media_type(ext) == "video":
                has_video = True
            asset_id = _upload_asset(media_file, "Reference media file")
            asset_list.append(f"{asset_id}")
            media_content += f'<{media_type(ext)} src="data:{mime_type(ext)};asset_id,{asset_id}" />'

        if has_video:
            assert len(media_files) == 1, "Only single video supported."

        asset_seq = ",".join(asset_list)
        print(f"Assets uploaded: {asset_seq}")

        headers = {
            "Authorization": f"Bearer {kApiKey}",
            "Content-Type": "application/json",
            "NVCF-INPUT-ASSET-REFERENCES": asset_seq,
            "NVCF-FUNCTION-ASSET-IDS": asset_seq,
            "Accept": "application/json" if not stream else "text/event-stream",
        }

        messages = [
            {
                "role": "user",
                "content": f"{query} {media_content}",
            }
        ]
        payload = {
            "max_tokens": 256,
            "temperature": 0.2,
            "top_p": 0.7,
            "seed": 50,
            "num_frames_per_inference": 8,
            "messages": messages,
            "stream": stream,
            "model": "nvidia/vila",
        }

        response = requests.post(infer_url, headers=headers, json=payload, stream=stream)
        if stream:
            for line in response.iter_lines():
                if line:
                    print(line.decode("utf-8"))
        else:
            print(response.json())
            return response.json()

        print(f"Deleting assets: {asset_list}")
        for asset_id in asset_list:
            _delete_asset(asset_id)


    # Run the main inference
    vila_output = chat_with_media_nvcf(invoke_url, media_samples, vila_prompt, stream)
    image_summary = str(vila_output['choices'][0]['message']['content'])
    print("Summary:")
    print(image_summary)

    return image_summary
