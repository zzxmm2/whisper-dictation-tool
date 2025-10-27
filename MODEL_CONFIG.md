# Whisper Model Configuration Guide

## Model Size Options

You can easily change the model size by editing the `MODEL_SIZE` variable in `dictation.py`:

```python
self.MODEL_SIZE = "medium"  # Change this to balance accuracy vs. speed
```

## Model Comparison

| Model | Speed | Accuracy | Memory | Best For |
|-------|-------|----------|---------|----------|
| **base** | ⚡⚡⚡ | ⭐⭐ | 💾 | Quick dictation, basic accuracy |
| **small** | ⚡⚡ | ⭐⭐⭐ | 💾💾 | Balanced speed/accuracy |
| **medium** | ⚡ | ⭐⭐⭐⭐ | 💾💾💾 | **Mixed languages, high accuracy** |
| **large** | 🐌 | ⭐⭐⭐⭐⭐ | 💾💾💾💾 | Best accuracy, slowest |

## Recommended Settings

### 🚀 **For Speed (Low Latency)**
```python
self.MODEL_SIZE = "base"  # Fastest, decent accuracy
```

### ⚖️ **For Balance**
```python
self.MODEL_SIZE = "small"  # Good speed, good accuracy
```

### 🎯 **For Mixed Languages (Current)**
```python
self.MODEL_SIZE = "small"  # Best balance for Chinese-English mixed speech
```

### 🏆 **For Maximum Accuracy**
```python
self.MODEL_SIZE = "large"  # Best accuracy, slowest
```

## How to Change

1. Open `dictation.py` in any text editor
2. Find line 27: `self.MODEL_SIZE = "small"`
3. Change `"small"` to your preferred model size
4. Save the file
5. Restart the dictation tool

## Performance Impact

- **First Run**: Larger models take longer to download and load
- **Transcription Speed**: Larger models are slower but more accurate
- **Memory Usage**: Larger models use more RAM
- **Mixed Language**: Medium+ models handle Chinese-English much better

## Current Setting

Your app is currently set to use the **small** model, which provides:
- ✅ Good mixed language accuracy
- ✅ Good traditional→simplified Chinese conversion
- ✅ Balanced speed and accuracy
- ✅ Moderate memory usage

This is a great choice for most users who want good accuracy without the latency of larger models.
