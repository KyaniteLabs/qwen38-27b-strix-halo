# Vision battery v5 — Q4 quant produces degenerate visual output (2026-08-19)

## Finding
Qwen3.8-27B at Q4_K_XL quant + mmproj-F16.gguf: ALL 6 vision questions return
the same repeated slash characters (`//////...`) with fr=length, think=0ch.
The vision API pipeline works correctly (no decode errors, no 400s, images
received and processed). The output is a consistent degenerate pattern across
ALL images (colors, gradients, system graphs).

## Architecture context
- MODEL GGUF (866 tensors): language model only, Q4_K_XL quant
- MMPROJ GGUF (334 tensors): 27-layer ViT + projection, F16 precision
- Vision embeddings from F16 mmproj are injected into the Q4 model's context
- The Q4-quantized language model cannot correctly process these embeddings

## Implication
Vision on this rig requires a higher model quant (Q8_0 or above). The Q4_K_XL
champion is text-only in practice. Vision-capable serving needs either:
(a) a separate higher-quant model for vision tasks, or
(b) a mixed-quant approach that preserves vision-capable precision, or
(c) acceptance that the $1,400 rig's vision lane requires trade-offs

## Conditions
GMKtec EVO-X2 ($1,400), Ryzen AI Max+ 395, 96GB unified. Q4_K_XL + q4_0 KV.
MTP n12 + ngram capped. llama.cpp dflash fork. PIL-generated JPEGs (confirmed
compatible with stb_image decoder). 6 questions × 300 max tokens.
