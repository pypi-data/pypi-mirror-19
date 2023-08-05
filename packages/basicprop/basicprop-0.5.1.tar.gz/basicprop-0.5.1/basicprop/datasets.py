import numpy as np

BG_PIXEL = 0
FG_PIXEL = 255
dtype = np.uint8

def get_epoch_labels(lo, hi, batch_size, num_batches, shuffle=True, seed=None):

    if seed is not None:
        np.random.seed(seed)

    labels = np.random.randint(lo, hi, batch_size * num_batches, dtype=dtype)
    
    if shuffle:
        np.random.shuffle(labels)

    return labels

def get_batch_labels(labels, num_batches, shuffle=True, seed=None):

    if seed is not None:
        np.random.seed(seed)

    labels = np.split(labels, num_batches)
    
    if shuffle:
        np.random.shuffle(labels)

    return labels

class Rects(object):
    num_labels = 100

    def get_image(self, y, width=10):
        y1 = y / 10
        y2 = y % 10

        # Configuration
        x1offset = 3
        x2offset = 15
        heights = np.array([3, 5, 7, 9, 11, 13, 15, 17, 19, 21])
        
        # Create Background
        x = np.full((28, 28), BG_PIXEL, dtype=dtype)
        
        # Create Foreground
        line1 = np.full((heights[y1], width), FG_PIXEL, dtype=dtype)
        x[3:3+heights[y1],x1offset:x1offset+width] = line1
        
        line2 = np.full((heights[y2], width), FG_PIXEL, dtype=dtype)
        x[3:3+heights[y2],x2offset:x2offset+width] = line2
        
        return x

    def get_batch(self, batch_size, labels=None, seed=None):
        """ First randomly select labels, then generate images
            based on labels and concatenate to create batch.
        """

        if seed is not None:
            np.random.seed(seed)

        if labels is None:
            labels = np.random.randint(0, self.num_labels, batch_size, dtype=dtype)

        assert len(labels) == batch_size, "{} != {}".format(len(labels), batch_size)
        
        data = []
        for y in labels:
            x = self.get_image(y)
            data.append(x.reshape(-1))
        data = np.concatenate([np.expand_dims(x, axis=0) for x in data], axis=0).astype(dtype)
        return (data, labels)

    def get_epoch(self, batch_size, num_batches, shuffle=True, seed=None):
        labels = get_epoch_labels(0, self.num_labels, batch_size, num_batches, shuffle=shuffle, seed=seed)
        labels = get_batch_labels(labels, num_batches, shuffle=shuffle, seed=seed)
        
        for i in range(num_batches):
            yield self.get_batch(batch_size, labels=labels[i], seed=seed)

class Line(object):
    num_labels = 10

    def get_image(self, y, width=4):
        x = np.full((28, 28), BG_PIXEL, dtype=dtype)
        offset = y * 2
        line = np.full((28,width), FG_PIXEL, dtype=dtype)
        x[:,(offset+3):(offset+3+width)] = line
        return x    

    def get_batch(self, batch_size, labels=None, seed=None):
        """ First randomly select labels, then generate images
            based on labels and concatenate to create batch.
        """

        if seed is not None:
            np.random.seed(seed)

        if labels is None:
            labels = np.random.randint(0, self.num_labels, batch_size, dtype=dtype)

        assert len(labels) == batch_size, "{} != {}".format(len(labels), batch_size)

        data = []
        for y in labels:
            x = self.get_image(y)
            data.append(x.reshape(-1))
        data = np.concatenate([np.expand_dims(x, axis=0) for x in data], axis=0).astype(dtype)
        return (data, labels)

    def get_epoch(self, batch_size, num_batches, shuffle=True, seed=None):
        labels = get_epoch_labels(0, self.num_labels, batch_size, num_batches, shuffle=shuffle, seed=seed)
        labels = get_batch_labels(labels, num_batches, shuffle=shuffle, seed=seed)
        
        for i in range(num_batches):
            yield self.get_batch(batch_size, labels=labels[i], seed=seed)
