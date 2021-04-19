# Code for Discard Noisy Instance Dynamically
# Inspired by Sangwook, Taheyeon

import torch
import numpy as np
from sklearn import metrics
from sklearn import cluster
from tqdm import tqdm

from .svd_classifier import get_singular_value_vector
from .svd_classifier import singular_label
from .svd_classifier import kmean_singular_label

def same_score(v_ortho_dict, model_represents, label):
    model_represents = torch.from_numpy(model_represents).cuda()
    scores = torch.zeros(model_represents.shape[0])
    
    for i, data in enumerate(model_represents):
        scores[i] = torch.dot(v_ortho_dict[label[i]][0], data/torch.norm(data)).abs()
    return scores

def same_topk(label_list, scores, p):
    
    output = []
    for idx in range(len(np.unique(label_list))):
        num_inst = int(p * np.sum(label_list==idx))
        indexs = torch.tensor(range(50000))[label_list==idx]
        tmp_sort, tmp_idx = torch.sort(scores[label_list==idx], descending=False)
        # 못 들어간 애가 필요한거니까 이렇게!
        output += indexs[tmp_idx[num_inst:]].numpy().tolist()
        
    return torch.tensor(output).long()

def same_topk_index(label_list, out_list, p):
    
    singular_dict, v_ortho_dict = get_singular_value_vector(label_list, out_list)
    for key in v_ortho_dict.keys():
        v_ortho_dict[key] = v_ortho_dict[key].cuda()
        
    scores = same_score(v_ortho_dict, out_list, label_list)
    output = same_topk(label_list, scores, p)
    return output.numpy()

def compute_noisy_ratio(data_loader):
    isNoisy_list = np.empty((0,))
    
    with tqdm(data_loader) as progress:
        for _, (_, label, index, label_gt) in enumerate(progress):
            isNoisy = label == label_gt
            isNoisy_list = np.concatenate((isNoisy_list, isNoisy.cpu()))

    print ('#############################')
    print (isNoisy_list.sum(), isNoisy_list.shape)
    print('purity in this dataset: {}'.format(isNoisy_list.sum() / isNoisy_list.shape))
    