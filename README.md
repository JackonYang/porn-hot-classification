# porn-hot-classification

Tensorflow 版本的图片鉴黄。not suitable/safe for work (NSFW) images detection using Tensorflow


# Working Log


## 建立基线模型 baseline model

2020.02.28 done [baseline_model_v0.ipynb](baseline_model_v0.ipynb)

training accuracy: 90%, validation accuracy: 66%

total timecost: ~6min

Next Steps:

- [x] 一边读大图，一边 resize，训练太慢。尝试用 tf.records 优化 或者预先 resize 图片
- [x] noisy label 很多，试一下 learning with noisy label (LNL) 模型


## 数据预处理

#### 处理方法

1. 删除无效图片 （ filesize < 10k )
2. 非 RGB 模式到转为 RBG，保证 channel 数一致
2. resize 到 256x256，丢弃读取失败到图片. `image file is truncated (x bytes not processed)`


```bash
$ cd /home/jackon/datasets/porn_hot_images/original_images
$ find . -type f -size -10k -exec mv {} ../invalid/ \;
$ time python resize_images.py

real	58m38.114s
user	56m48.656s
sys	1m11.584s
```

resize 处理的速度是 每 30 秒 1000 张图片，

首批 3 个 类别共约 100k 张图片，耗时 50min

#### 处理后的训练效果

使用 resize 后的 image 训练，速度提高 10x。

1. 每个 step 耗时从 3s 降至 0.3s
2. 每个 epoch 从 74s 降至 6-7s


## Learning with noisy label


#### 思路

1. 用部分数据（10k/label）train 一个 model，
2. 用这个 model 预测其他数据，取 accuracy > 95% 且与标注相同的数据作为新的 labeled data
3. 用新的 labeled data 作为新的训练数据，重复 1-2 步。


#### 初步验证

结论：可行。

用训练的模型 inference 原始数据集，可以帮助选出 30% 质量极高的 ground truth data。

过滤条件 prediction accuracy > 95%, 且预测与已有标注相同。

验证代码及结果预览: [learning-with-noisy-lable-v0.ipynb](learning-with-noisy-lable-v0.ipynb)


Next Steps:

- [ ] 用筛出的 30% 高质量 label 数据重新训练模型。
- [ ] 用新模型找把握最大的 false label，甚至预测正确的 label。
- [ ] 将修正过的数据加入训练集合，重复以上步骤
