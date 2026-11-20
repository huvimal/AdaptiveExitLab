import numpy as np
from common import *

def run():
    import torch
    torch.manual_seed(14);torch.set_num_threads(2);x,y,vx,vy,tx,ty=classification(14)
    first=torch.nn.Linear(8,16);early=torch.nn.Linear(16,1);second=torch.nn.Linear(16,16);late=torch.nn.Linear(16,1)
    opt=torch.optim.Adam(list(first.parameters())+list(early.parameters())+list(second.parameters())+list(late.parameters()),lr=.02)
    a=torch.tensor(x,dtype=torch.float32);labels=torch.tensor(y,dtype=torch.float32)
    def forward(z):
        h=torch.relu(first(z));return early(h).squeeze(-1),late(torch.relu(second(h))).squeeze(-1)
    for _ in range(120):
        e,l=forward(a);loss=torch.nn.functional.binary_cross_entropy_with_logits(e,labels)+torch.nn.functional.binary_cross_entropy_with_logits(l,labels)
        opt.zero_grad();loss.backward();opt.step()
    with torch.no_grad():ev,lv=[torch.sigmoid(t).numpy() for t in forward(torch.tensor(vx,dtype=torch.float32))]
    candidates=[]
    for t in [.6,.7,.8,.9,.95]:
        confident=np.maximum(ev,1-ev)>=t;p=np.where(confident,ev,lv);candidates.append((measures(vy,p)['accuracy'],float(confident.mean()),t))
    _,_,threshold=max(candidates)
    z=torch.tensor(tx,dtype=torch.float32)
    with torch.no_grad():
        h=torch.relu(first(z));pe=torch.sigmoid(early(h)).squeeze(-1);mask=torch.maximum(pe,1-pe)<threshold
        p=pe.clone();p[mask]=torch.sigmoid(late(torch.relu(second(h[mask])))).squeeze(-1)
        full=torch.sigmoid(late(torch.relu(second(h)))).squeeze(-1)
    return {'adaptive':measures(ty,p.numpy()),'full_depth':measures(ty,full.numpy()),'selected_confidence':threshold,
            'early_exit_fraction':float((~mask).float().mean()),'late_rows_computed':int(mask.sum()),
            'checks':[check(int(mask.sum())<=len(tx),'Late stage only executes uncertain rows')],
            'scope':'Real trained two-stage MLP on synthetic numeric alerts, validation-selected confidence. Fraction exiting is not a measured latency speedup.'}
