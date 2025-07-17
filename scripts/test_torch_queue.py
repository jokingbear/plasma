import sys
sys.path.append('./')

import plasma.torch.parallel as ptp
import torch


class Pipe(ptp.TorchPipe):
    
    def run(self, rank):
        a = torch.randn(10, 1000, dtype=torch.float, device=f'cuda:{rank}')
        
        def run(x):
            y = a * x
            return y.cpu().numpy()
        return run


if __name__ == '__main__':
    ptp.init()
    
    queue = ptp.CudaQueue(num_runner=2).register_callback(Pipe()).chain(print).run()
    
    for i in range(100):
        queue.put(i)
    
    queue.release()
