from setuptools import setup
setup(  
    name = 'linovelib',  
    version = '0.0.3', 
    description = 'Download novel from linovelib',  
    license = 'MIT License',  
    install_requires = ["bs4","fire","requests","fake_useragent","pypandoc"], 
    packages = ['linovelib'],  # 要打包的项目文件夹
    include_package_data=True,   # 自动打包文件夹内所有数据
    author = 'Lensit',  
    author_email = '1570515219@qq.com',
    url = 'https://gitee.com/lensit/linovelib',
    entry_points={"console_scripts": ["linovelib = linovelib.__main__:main"]},
    zip_safe=True
)  

