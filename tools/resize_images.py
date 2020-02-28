import os
from PIL import Image

source_dir = '/home/jackon/datasets/porn_hot_images/original_images'
target_dir = '/home/jackon/datasets/porn_hot_images/resized-256x256'

target_size = (256, 256)
name_subfix = '.256x256.jpg'


def main(source_dir, target_dir):
    for label in os.listdir(source_dir):
        label_src = os.path.join(source_dir, label)
        label_target = os.path.join(target_dir, label)
        if not os.path.exists(label_target):
            os.makedirs(label_target)

        label_images = os.listdir(label_src)
        label_images_count = len(label_images)
        cnt = 0

        print('=== start processing %s. count = %s' % (label, label_images_count))
        for img in label_images:
            cnt += 1
            if cnt % 1000 == 0:
                print('(%s/%s) processing %s' % (cnt, label_images_count, img))
                # break  # for test
            try:
                im_src = os.path.join(label_src, img)
                im = Image.open(im_src)
                if im.mode != 'RGB':
                    im = im.convert('RGB')
                new_im = im.resize(target_size)
                new_name = os.path.join(label_target, img + name_subfix)
                new_im.save(new_name)
            except Exception as e:
                print('!!! skip image! %s' % im_src)
                print(e)


if __name__ == '__main__':
    main(source_dir, target_dir)
