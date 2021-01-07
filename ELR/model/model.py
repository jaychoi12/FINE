import torch.nn as nn
import torch.nn.functional as F
from base import BaseModel
from .ResNet_Zoo import ResNet, BasicBlock, Bottleneck

def resnet8(num_classes=10):
    return ResNet(BasickBlock, [1,1,1,1], num_classes=num_classes)

def resnet18(num_classes=10):
    return ResNet(BasicBlock, [2,2,2,2], num_classes=num_classes)

def resnet34(num_classes=10):
    return ResNet(BasicBlock, [3,4,6,3], num_classes=num_classes)

def resnet50(num_classes=10):
    return ResNet(Bottleneck, [3,4,6,3], num_classes=num_classes)

def resnet101(num_classes=10):
    return ResNet(Bottleneck, [3,4,23,3], num_classes=num_classes)