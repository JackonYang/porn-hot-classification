# porn-hot-classification

Tensorflow 版本的图片鉴黄。not suitable/safe for work (NSFW) images detection using Tensorflow


# Working Log


## 建立基线模型 baseline model

2020.02.28 done [baseline_model_v0.ipynb](baseline_model_v0.ipynb)

training accuracy: 90%, validation accuracy: 66%

total timecost: ~6min

Next Steps:

1. 一边读大图，一边 resize，训练太慢。尝试用 tf.records 优化 或者预先 resize 图片
2. noisy label 很多，试一下 learning with noisy label (LNL) 模型


## 数据预处理

#### 处理方法

1. 删除无效图片 （ filesize < 10k )
2. 非 RGB 模式到转为 RBG，保证 channel 数一致
2. resize 到 256x256，丢弃读取失败到图片. `image file is truncated (x bytes not processed)`


```bash
$ cd /home/jackon/datasets/porn_hot_images/original_images
$ find . -type f -size -10k -exec mv {} ../invalid/ \;
$ time python resize_images.py
```

resize 处理的速度是 每 30 秒 1000 张图片，

首批 3 个 类别共约 100k 张图片，耗时 50min

#### 处理后的训练效果

使用 resize 后的 image 训练，速度提高 10x。

1. 每个 step 耗时从 3s 降至 0.3s
2. 每个 epoch 从 74s 降至 6-7s
