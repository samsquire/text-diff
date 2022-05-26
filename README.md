# text-diff
This is a python impelementation of three way merge that uses Myers algorithm.

```
common = Document(root_text, None)

S = Document(original, common)

document_left1 = Document(left1, S)
document_left2 = Document(left2, document_left1)

document_right1 = Document(right1, S)
document_right2 = Document(right2, document_right1)

merged = diff3(document_left2, document_right2)
print("merged", merged.text)
```

Apply a diff and apply it to the source document.
```
print(diff_and_apply(original, left2))
```
