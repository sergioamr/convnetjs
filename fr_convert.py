import os

import numpy
import imageio

import random

from skimage import data, color
from skimage.transform import rescale, resize, downscale_local_mean

data_folder = "/classifier"
xs = []
ys = []

full_path = os.getcwd() + data_folder

labels = []
labels_name = []
file_paths = []

batch_size = 100
img_dimension = 64

img_size = img_dimension * img_dimension

#labels_list = ["rock", "fraggle", "empty", "food"]

max_value = 0

classes_list = []

for directory in os.listdir(full_path):
    dir = os.path.join(full_path, directory)
    onlyfiles = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    label_paths = []

    if (len(onlyfiles) > 0):
        for i in range(len(onlyfiles)):
            path_file = dir + "/" + onlyfiles[i]
            label_paths.append(path_file)

        classes_list.append(label_paths)
        labels_name.append(directory)

        #if (directory != "food"):
        max_value = max( len(onlyfiles), max_value )

batch_set = 0
for f in classes_list:
    print("%d:: --- %s ---" % (batch_set, labels_name[batch_set]))
    y = classes_list[batch_set]
    x = [batch_set] * len(y)

    labels.extend(x[:max_value])
    file_paths.extend(y[:max_value])

    print file_paths

    batch_set +=1

print("### %d ###" % max_value)

print("### LABELS ###")
for i in range(len(labels_name)):
    print(" %i: %s " %(i, labels_name[i]))

print("### TOTAL FILES  ###")
print(" %i" %(len(file_paths)))

output_path = os.getcwd() + "/output/"

######## Randomize set #########
combined = list(zip(labels, file_paths))
random.shuffle(combined)
labels[:], file_paths[:] = zip(*combined)

batches_n = len(file_paths) / batch_size

########## Save labels #########
# dump the labels

network_name = "network_64_big"
dataset_name = "output"

L = 'var labels=' + `list(labels[:])` + ';\n'
L += 'var classes_txt=['
for i in range(len(labels_name)):
    if (i != 0):
        L += ","
    L += "\"" + labels_name[i] + "\""
L +=  '];\n'

L += 'var dataset_name="%s";\n' % dataset_name
L += 'var network_name="%s";\n' % network_name

L += 'var num_samples_per_batch=%i;\n' % batch_size
L += 'var image_dimension=%i;\n' % img_dimension
L += 'var test_batch=%i;\n' % (batches_n - 1)
L += 'var num_batches=%i;\n' % (batches_n)

open(output_path + 'fr_labels.js', 'w').write(L)

N = "layer_defs = []; \n"
N += "layer_defs.push({type:'input', out_sx:%d, out_sy:%d, out_depth:3}); \n" % (img_dimension, img_dimension)
N += "layer_defs.push({type:'conv', sx:5, filters:32, stride:1, pad:2, activation:'relu'}); \n"
N += "layer_defs.push({type:'pool', sx:2, stride:2}); \n"
N += "layer_defs.push({type:'conv', sx:5, filters:40, stride:1, pad:2, activation:'relu'}); \n"
N += "layer_defs.push({type:'pool', sx:2, stride:2}); \n"
N += "layer_defs.push({type:'conv', sx:5, filters:40, stride:1, pad:2, activation:'relu'}); \n"
N += "layer_defs.push({type:'pool', sx:2, stride:2}); \n"
N += "layer_defs.push({type:'softmax', num_classes: %d }); \n" % len(labels_name)
N += " \n"
N += "net = new convnetjs.Net(); \n"
N += "net.makeLayers(layer_defs); \n"
N += " \n"
N += "trainer = new convnetjs.SGDTrainer(net, {method:'adadelta', batch_size:%d, l2_decay:0.0001}); \n" % (batches_n)

open(output_path + 'fr_network.js', 'w').write(N)

########## Create batch #########

xs = []
print xs

print("------ NUM BATCHES %i ------" % batches_n)

b = 0
for i in range(len(file_paths)):
#for i in range(3):

    im = imageio.imread(file_paths[i])
    im_resized = image_rescaled = resize(im, (img_dimension, img_dimension, 3), mode='reflect')
    rescaled_image = 255 * im_resized
    im_resized = rescaled_image.astype(numpy.uint8)

    xarr = im_resized[:, :, :]
    #imageio.imwrite(output_path + "%i.png" %i, xarr)

    if i == 0:
        xs = xarr

    if (i % 50 == 0):
        print("%i : -----------" %i)
        print xs.shape

    if (i != 0 and i % (batch_size) == 0):
        print("+ %i/%i ::: Batch ::: " % (i, batches_n))

        xv = xs[:((img_size*batch_size)/img_dimension), :, :]
        print xv.shape

        x = xv.reshape(batch_size,img_size,3)
        imageio.imwrite(output_path + "output_batch_%i.png" % b, x)

        b = int(i / batch_size)
        xs = xarr
    else:
        xs = numpy.concatenate((xs, xarr))

