# file-selector

Select and bundle files into single text output. Useful for sharing code with models like o1/o3 which don't accept file uploads.

## Usage

```bash
python file_selector.py .py .txt
```

Commands:
```
e d1       # expand directory number 1
c d1       # collapse directory number 1
ca         # collapse all directories
s f1 f2    # toggle selection of files 1 and 2
sd d1      # select all files in directory 1
w          # write selection to output.txt
q          # quit (writes output too)
```

Numbers are shown as:
```
[ ] d1. + folder/     # directory
[*] f2. file.txt     # selected file
[ ] f3. other.py     # unselected file
```

## Output

Creates `output.txt` with format:
```
===== START OF FILE ./file.py =====
content
===== END OF FILE ./file.py =====
```
