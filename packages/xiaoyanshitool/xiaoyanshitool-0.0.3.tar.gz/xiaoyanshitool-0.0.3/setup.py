#!/usr/bin/env python
# encoding: UTF-8

'''
__   ___________________________________________
| \  ||______   |   |______|_____||______|______
|  \_||______   |   |______|     |______||______

________     __________________________  _____ _     _
|  |  ||     ||______  |  |      |_____]|     | \___/
|  |  ||_____|______|__|__|_____ |_____]|_____|_/   \_
+ ------------------------------------------ +
|                smiletools                  |
+ ------------------------------------------ +
|                                            |
|   ++++++++++++++++++++++++++++++++++++++   |
|   ++++++++++++++++++++++++++++++++++++++   |
|   ++++++++++++++++++++++++++++++++++++++   |
|   ++++++++++++++++++++++++++++++++++++++   |
|   ++++++++++++++++++++++++++++++++++++++   |
|                                            |
|   useful api                               |
+ ------------------------------------------ +
'''

from setuptools import setup, find_packages

setup(
      name='xiaoyanshitool',   #名称
      version='0.0.3',  #版本
      description="some useful api for xiaoyanshi and xiaoxingxing", #描述
      keywords='python excel ',
      author='Smile',  #作者
      author_email='smiletoye@gmail.com', #作者邮箱
      url='https://github.com/SmileLikeYe', #作者链接
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[      #需求的第三方模块
        'requests',
        'bs4',
        'xlwt',
      ],
      entry_points={
        'console_scripts':[     #如果你想要以Linux命令的形式使用
            'xiaoyanshitool = xiaoyanshitool.xiaoyanshitool:main'
        ]
      },
)
