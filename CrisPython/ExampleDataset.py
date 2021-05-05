import DatasetModule
from torch.utils.data import DataLoader
import time
import psutil
import multiprocessing
DM = DatasetModule.VideoDataset(["Train"],256)
NUM_WORKERS = multiprocessing.cpu_count()
Test = DataLoader(DM, batch_size=128, num_workers=16,shuffle=True)

print("Primera Pasada: Random")
tt = time.time()
i=0
for t in Test:
    print(i,flush=True)
    print(time.time() - tt,flush=True)
    #print(psutil.virtual_memory().percent,flush=True)
    #if i%5==0:
    i+=1
    tt = time.time()
print(time.time() - tt,flush=True)
#
#
# DM = DatasetModule.VideoDataset(["HCULB_00181","HCULB_00311","HCULB_00073","HCULB_00118","HCULB_00206"],256)
# Test = DataLoader(DM, batch_size=128, num_workers=NUM_WORKERS,shuffle=True)
#
# print("Segunda Pasada: Random")
# tt = time.time()
# i=0
# for t in Test:
#     #print(psutil.virtual_memory().percent,flush=True)
#     #if i%5==0:
#     #    print(i)
#     i+=1
#     #tt = time.time()
# print(time.time() - tt)
#
# Test = DataLoader(DM, batch_size=128, num_workers=NUM_WORKERS)
#
# print("Primera Pasada: Lineal")
# tt = time.time()
# i=0
# for t in Test:
#     #print(psutil.virtual_memory().percent,flush=True)
#     #if i%5==0:
#     #    print(i)
#     i+=1
#     #tt = time.time()
# print(time.time() - tt)
#
# print("Segunda Pasada: Lineal")
# tt = time.time()
# i=0
# for t in Test:
#     #print(psutil.virtual_memory().percent,flush=True)
#     #if i%5==0:
#     #    print(i)
#     i+=1
#     #tt = time.time()
# print(time.time() - tt)
