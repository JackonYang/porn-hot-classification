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
