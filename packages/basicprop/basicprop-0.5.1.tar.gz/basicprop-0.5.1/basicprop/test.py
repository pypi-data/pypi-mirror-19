import unittest

import numpy as np
import datasets
import noise

def all_equal(a1, a2):
    return all(x1 == x2 for x1, x2 in zip(a1, a2))

def check_random_batch_labels(dataset, seed=123):
    batch_size = 16
    _, labels1 = dataset.get_batch(batch_size, seed=seed)
    _, labels2 = dataset.get_batch(batch_size, seed=seed)
    assert all_equal(labels1, labels2)

def check_random_epoch_labels(dataset, seed=123):
    batch_size = 16
    num_batches = 10
    e1 = dataset.get_epoch(batch_size, num_batches, shuffle=True, seed=seed)
    e2 = dataset.get_epoch(batch_size, num_batches, shuffle=True, seed=seed)
    for (_, labels1), (_, labels2) in zip(e1, e2):
        assert all_equal(labels1, labels2)

class DataTestCase(unittest.TestCase):

    def test_random_batch_labels(self):
        seed = 11
        check_random_batch_labels(datasets.Line(), seed)
        check_random_batch_labels(datasets.Rects(), seed)

    def test_random_epoch_labels(self):
        seed = 11
        check_random_epoch_labels(datasets.Line(), seed)
        check_random_epoch_labels(datasets.Rects(), seed)

if __name__ == '__main__':
    unittest.main()
