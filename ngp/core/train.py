
from ngp.core.godot import GodotSim

import torch
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from cantilever.core.timer import timeit, timeiterator, show_timings


class Training:
    def __init__(self):
        pass

    def dataloader(self):
        return DataLoader(
            dataset=GodotSim(n=64*10),
            batch_size=16,
            shuffle=False,
            num_workers=4,
            collate_fn=GodotSim.collate,
            sampler=None
        )

    def train(self, epoch):
        with timeit("init"):
            loader = self.dataloader()

            for i in range(epoch):
                with timeit("epoch"):
                    for batch in timeiterator(iter(loader)):
                        
                        images, bones = batch

                        print(len(images), images.shape, len(bones), bones.shape)


                        with timeit("step"):
                            self.step()

        show_timings(True)

    def step(self):
        pass


def main():
    
    t = Training()

    t.train(10)



if __name__ == "__main__":
    main()
