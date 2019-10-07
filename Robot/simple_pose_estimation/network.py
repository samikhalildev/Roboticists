'''
This code a heavily modified version of MobileNet OpenPose:
https://github.com/ildoonet/tf-pose-estimation

This code is a port of the Tensorflow model and weights to pure numpy without any Tensorflow dependencies.
'''
import numpy as np
import os

val_cache_file_path = os.path.join(os.path.dirname(__file__), 'val_cache.npz')
cached_vals = None

if os.path.exists(val_cache_file_path):
    cached_vals = dict(np.load(val_cache_file_path).items())

def conv32(ar, k, origin):
    ox, oy = origin
    ox = ox - 1
    oy = oy - 1
    x, y, d = ar.shape
    mat_dim = (x/2*y/2, d)

    ap = np.pad(ar, [(2,3),(2,3),(0,0)], mode='constant')
    result = np.matmul(ap[ox + 2:ox - 3:2, oy + 2:oy - 3:2].reshape(mat_dim), k[2,2]) + \
             np.matmul(ap[ox + 3:ox - 2:2, oy + 2:oy - 3:2].reshape(mat_dim), k[1,2]) + \
             np.matmul(ap[ox + 4:ox - 1:2, oy + 2:oy - 3:2].reshape(mat_dim), k[0,2]) + \
             np.matmul(ap[ox + 2:ox - 3:2, oy + 3:oy - 2:2].reshape(mat_dim), k[2,1]) + \
             np.matmul(ap[ox + 3:ox - 2:2, oy + 3:oy - 2:2].reshape(mat_dim), k[1,1]) + \
             np.matmul(ap[ox + 4:ox - 1:2, oy + 3:oy - 2:2].reshape(mat_dim), k[0,1]) + \
             np.matmul(ap[ox + 2:ox - 3:2, oy + 4:oy - 1:2].reshape(mat_dim), k[2,0]) + \
             np.matmul(ap[ox + 3:ox - 2:2, oy + 4:oy - 1:2].reshape(mat_dim), k[1,0]) + \
             np.matmul(ap[ox + 4:ox - 1:2, oy + 4:oy - 1:2].reshape(mat_dim), k[0,0])
    result = result.reshape((x/2,y/2,-1))
    return result

def sconv3(ar, k, origin):
    # This is the slowest operation
    # A private C implemenentation is in magic_c_helpers
    ox, oy = origin
    ox = ox - 1
    oy = oy - 1
    k = k.reshape([3,3,-1])
    ap = np.pad(ar, [(2,3),(2,3),(0,0)], mode='constant')
    result = ap[ox + 2:ox - 3, oy + 2:oy - 3] * k[2,2] + \
             ap[ox + 3:ox - 2, oy + 2:oy - 3] * k[1,2] + \
             ap[ox + 4:ox - 1, oy + 2:oy - 3] * k[0,2] + \
             ap[ox + 2:ox - 3, oy + 3:oy - 2] * k[2,1] + \
             ap[ox + 3:ox - 2, oy + 3:oy - 2] * k[1,1] + \
             ap[ox + 4:ox - 1, oy + 3:oy - 2] * k[0,1] + \
             ap[ox + 2:ox - 3, oy + 4:oy - 1] * k[2,0] + \
             ap[ox + 3:ox - 2, oy + 4:oy - 1] * k[1,0] + \
             ap[ox + 4:ox - 1, oy + 4:oy - 1] * k[0,0]
    return result

def sconv32(ar, k, origin):
    ox, oy = origin
    ox = ox - 1
    oy = oy - 1
    k = k.reshape([3,3,-1])
    ap = np.pad(ar, [(2,3),(2,3),(0,0)], mode='constant')
    result = ap[(ox + 2):(ox - 3):2, (oy + 2):(oy - 3):2] * k[2,2] + \
             ap[(ox + 3):(ox - 2):2, (oy + 2):(oy - 3):2] * k[1,2] + \
             ap[(ox + 4):(ox - 1):2, (oy + 2):(oy - 3):2] * k[0,2] + \
             ap[(ox + 2):(ox - 3):2, (oy + 3):(oy - 2):2] * k[2,1] + \
             ap[(ox + 3):(ox - 2):2, (oy + 3):(oy - 2):2] * k[1,1] + \
             ap[(ox + 4):(ox - 1):2, (oy + 3):(oy - 2):2] * k[0,1] + \
             ap[(ox + 2):(ox - 3):2, (oy + 4):(oy - 1):2] * k[2,0] + \
             ap[(ox + 3):(ox - 2):2, (oy + 4):(oy - 1):2] * k[1,0] + \
             ap[(ox + 4):(ox - 1):2, (oy + 4):(oy - 1):2] * k[0,0]
    return result

def maxpool(inp):
    w, h, d = inp.shape
    inps = inp.reshape([int(w/2), 2, int(h/2), 2, d])
    result = np.max(np.max(inps, axis=3), axis=1)
    return result

def concat(inps):
    result = np.concatenate(inps, axis=2)
    return result

def net_convb2(inp):
    weights = cached_vals['MobilenetV1/Conv2d_0/weights']
    offset = cached_vals['MobilenetV1/Conv2d_0/Conv2D_bn_offset']
    result = conv32(inp, weights, (1,1))
    result = np.maximum(result + offset, 0)
    return result

def net_sepconv(inp, name, relu=True):
    # inp = inp.astype(np.float32)
    dweights = cached_vals[name + '_depthwise/depthwise_weights']
    pweights = cached_vals[name + '_pointwise/weights']
    offset = cached_vals[name + '_pointwise/Conv2D_bn_offset']
    result = sconv3(inp, dweights, (0,0))

    result = result.reshape((inp.shape[0] * inp.shape[1], -1))
    result = np.matmul(result, pweights)
    result = result.reshape((inp.shape[0], inp.shape[1], -1))

    if relu:
        result = np.maximum(result + offset, 0)
    else:
        result = result + offset
    return result

def net_sepnoconv(inp, name, relu=True):
    # inp = inp.astype(np.float32)
    dweights = cached_vals[name + '_depthwise/depthwise_weights']
    pweights = cached_vals[name + '_pointwise/weights']
    offset = cached_vals[name + '_pointwise/Conv2D_bn_offset']
    
    x, y, d = inp.shape
    result = (inp * dweights).reshape((x * y, d))
    result = np.matmul(result, pweights)
    result = result.reshape((x, y, -1))
    
    if relu:
        result = np.maximum(result + offset, 0)
    else:
        result = result + offset
    return result

def net_sepconv2(inp, name):
    # inp = inp.astype(np.float32)
    dweights = cached_vals[name + '_depthwise/depthwise_weights']
    pweights = cached_vals[name + '_pointwise/weights']
    offset = cached_vals[name + '_pointwise/Conv2D_bn_offset']
    result = sconv32(inp, dweights, (1,1))

    x, y, d = result.shape
    result = result.reshape((x * y, -1))
    result = np.matmul(result, pweights)
    result = result.reshape((x, y, -1))

    result = np.maximum(result + offset, 0)
    return result

def inference(img):
    global cached_vals
    if cached_vals is None:
        cached_vals = dict(np.load(val_cache_file_path).items())

    # Ensure that the input is float32 (a float64 will cascade through and hurt performance)
    img = img.astype(np.float32, copy=False)

    s = net_convb2(img)

    s   = net_sepconv(s, 'MobilenetV1/Conv2d_1')
    s   = net_sepconv2(s, 'MobilenetV1/Conv2d_2')
    s   = net_sepconv(s, 'MobilenetV1/Conv2d_3')
    s3p = maxpool(s)
    s   = net_sepconv2(s, 'MobilenetV1/Conv2d_4')
    s   = net_sepconv(s, 'MobilenetV1/Conv2d_5')
    s   = net_sepconv(s, 'MobilenetV1/Conv2d_6')
    s7  = net_sepconv(s, 'MobilenetV1/Conv2d_7')
    s   = net_sepconv(s7, 'MobilenetV1/Conv2d_8')
    s   = net_sepconv(s, 'MobilenetV1/Conv2d_9')
    s   = net_sepconv(s, 'MobilenetV1/Conv2d_10')
    s   = net_sepconv(s, 'MobilenetV1/Conv2d_11')

    sfc = concat([s3p, s7, s])

    def net_stage(inp, prefix):
        st = net_sepconv(inp, prefix + '_1')
        st = net_sepconv(st, prefix + '_2')
        st = net_sepconv(st, prefix + '_3')
        st = net_sepnoconv(st, prefix + '_4')
        st = net_sepnoconv(st, prefix + '_5', relu=False)
        return st

    sfc1 = net_stage(sfc, 'Openpose/MConv_Stage1_L1')
    sfc2 = net_stage(sfc, 'Openpose/MConv_Stage1_L2')
    
    l1_last = sfc1
    l2_last = sfc2
    for stage_id in range(5):
        prefix = 'Openpose/MConv_Stage%d' % (stage_id + 2)
        lfc = concat([l1_last, l2_last, sfc])
        
        lfc1 = net_stage(lfc, prefix + '_L1')
        lfc2 = net_stage(lfc, prefix + '_L2')
        
        l1_last = lfc1
        l2_last = lfc2

    final = concat([l2_last, l1_last])
    return final
