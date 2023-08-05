import numpy as np

class Rects(object):
    def get_image(self, y, width=10):
        y1 = y / 10
        y2 = y % 10

        # Configuration
        x1offset = 3
        x2offset = 15
        heights = np.array([3, 5, 7, 9, 11, 13, 15, 17, 19, 21])
        
        # Create Background
        x = np.zeros((28, 28))
        
        # Create Foreground
        line1 = np.ones((heights[y1], width))
        x[3:3+heights[y1],x1offset:x1offset+width] = line1
        
        line2 = np.ones((heights[y2], width))
        x[3:3+heights[y2],x2offset:x2offset+width] = line2
        
        return x

    def get_batch(self, batch_size):
        """ First randomly select labels, then generate images
            based on labels and concatenate to create batch.
        """
        labels = np.random.randint(0, 100, batch_size).astype(np.uint8)
        data = []
        for y in labels:
            x = self.get_image(y)
            data.append(x.reshape(-1))
        data = np.concatenate([np.expand_dims(x, axis=0) for x in data], axis=0).astype(np.float32)
        return (data, labels)

class Line(object):
    def get_image(self, y, width=4):
        x = np.zeros((28, 28))
        offset = y * 2
        line = np.ones((28,width))
        x[:,(offset+3):(offset+3+width)] = line
        return x    

    def get_batch(self, batch_size):
        """ First randomly select labels, then generate images
            based on labels and concatenate to create batch.
        """
        labels = np.random.randint(0, 10, batch_size).astype(np.uint8)
        data = []
        for y in labels:
            x = self.get_image(y)
            data.append(x.reshape(-1))
        data = np.concatenate([np.expand_dims(x, axis=0) for x in data], axis=0).astype(np.float32)
        return (data, labels)
        