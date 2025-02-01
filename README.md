# file-selector

Select and bundle files into single text output. Useful for sharing code with ChatGPT.

## Usage

```bash
python file_selector.py .py .txt
```

Commands:
```
e folder  # expand directory
c folder  # collapse directory
s 1 2 3   # select files
q         # quit
```

## Output

Creates `output.txt` with format:
```
===== START OF FILE ./file.py =====
content
===== END OF FILE ./file.py =====
```