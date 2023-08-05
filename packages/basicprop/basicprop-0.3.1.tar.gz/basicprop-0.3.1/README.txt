# Basicprop (Synthetic Dataset)

## Instructions

There are the following datasets:

1. Line (10 classes)
2. Rects (100 classes)

Each dataset has the same API:

- get_image(y) -> returns an image of class y.
- get_batch(batch_size) -> returns a batch of images with random classes.

Here is an example:

```
from basicprop.datasets import Line, Rects

line = Line()
rects = Rects()

line_images = [line.get_image(y) for y in range(10)]
rects_images = [line.get_image(y) for y in range(100)]
```

## License

MIT
