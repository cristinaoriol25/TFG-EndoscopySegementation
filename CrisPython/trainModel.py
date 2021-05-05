import ClassifierMod
import DatasetModule
from torchvision import models, transforms
import torch
from torch.utils.data import DataLoader, Dataset
import pytorch_lightning as pl
from pytorch_lightning.loggers import TensorBoardLogger
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
import multiprocessing
import sys
# early_stop_callback = EarlyStopping(
#    monitor='val_loss',
#    min_delta=0.00,
#    patience=5,
#    verbose=False,
#    mode='min'
# )

version = sys.argv[1]
if version == '1':
    mode =True
    Fil = True
elif version == '2':
    mode = False
    Fil = True
elif version == '3':
    mode = True
    Fil = False
elif version == '4':
    mode = False
    Fil = False
NUM_WORKERS = multiprocessing.cpu_count()

tr = DatasetModule.VideoDataset(["Train"],256,mode)
vl = DatasetModule.VideoDataset(["Test"],256,mode)
train_loader = DataLoader(tr, batch_size=512, num_workers=40, shuffle=True)
val_loader = DataLoader(vl, batch_size=512, num_workers=40)

resnet = models.resnet50(pretrained=not Fil)

weight = tr.get_weight()

Net = ClassifierMod.SectionRecog(
        resnet,
        weight,
        image_size=256,
        hidden_layer='avgpool',
        projection_size=256,
        projection_hidden_size=4096,
        moving_average_decay=0.99
    )
if Fil:
    checkpoint = torch.load("/workspace/pazagra/SectRecong/FilterModel.ckpt")
    Net.load(checkpoint)


trainer = pl.Trainer(
        default_root_dir='checkpoints/',
        gpus=[0,1,2,3,4,5],
        num_nodes = 1,
        accelerator="dp",
        max_epochs=5,
        progress_bar_refresh_rate=1000,
        accumulate_grad_batches=1,
        sync_batchnorm=True,
        check_val_every_n_epoch=1
    )

for p in Net.learner.parameters():
    p.requires_grad = False
    
trainer.fit(Net, train_dataloader=train_loader, val_dataloaders=val_loader)

logger = TensorBoardLogger(save_dir="board/", name="Full"+version, version='bala
nced_'+version)

trainer = pl.Trainer(
        default_root_dir='checkpoints/',
        gpus=[0,1,2,3,4,5],
        num_nodes = 1,
        accelerator="dp",
        max_epochs=50,
        # callbacks=[early_stop_callback],
        progress_bar_refresh_rate=1000,
        accumulate_grad_batches=1,
        sync_batchnorm=True,
        logger = logger,
        check_val_every_n_epoch=1
    )

for p in Net.learner.parameters():
    p.requires_grad = True

trainer.fit(Net, train_dataloader=train_loader, val_dataloaders=val_loader)

trainer.save_checkpoint("Final_version"+version+".ckpt")
