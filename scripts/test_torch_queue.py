import sys
sys.path.append('./')

import plasma.torch.parallel as ptp
import torch


class Pipe(ptp.TorchPipe):
    
    def process_init(self, rank):
        a = torch.randn(10, 1000, dtype=torch.float, device=f'cuda:{rank}')
        self.anchor = a
    
    def run(self, x):
        y = self.anchor * x
        return y.cpu().numpy()



if __name__ == '__main__':
    ptp.init()
    
    queue = ptp.CudaQueue(num_runner=2).register_callback(Pipe()).chain(print).run()
    
    for i in range(100):
        queue.put(i)
    
    queue.release()
