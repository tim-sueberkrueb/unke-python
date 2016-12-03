# Unke

Python implementation of the Unke markup language

## Installation
```sh
python3 setup.py install    # Use sudo if necessary
```

# Usage
```unke
// myfile.unk

Root {
    some_numbers: [4,2,7,3]
    list_items: [
        ListItem {
            id: 1
            enabled: true
            description: "Hello World"
        }
    ]
}
```

```python
# myfile.py
import unke
doc = unke.load('myfile.unk')
root = doc.root
print(root.props['some_numbers'])
print(root.props['list_items'])
item_1 = root.props['list_items'][0]
print(item_1.props['description'])
```

## Licensing
Licensed under the terms of the MIT license.