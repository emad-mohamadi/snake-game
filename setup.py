from setuptools import setup, find_packages

name = 'snake'
version = '1.0.0'
description = 'snake-game, by Marboro team.'
long_description = """
Enjoy playing nostalgic snake game in your terminal.
GitHub: emad-mohamadi, melow-git, danial-fazel, Mhdig0
Any issues? Let us know: t.me/emad_mohammadi 
"""
author = "Marboro team"
author_email = "semadmhmdi@gmail.com"
url = "https://github.com/emad-mohamadi/terminal-tetris"
install_requires = ['keyboard', 'pygame']
package_data = {
    'snake': ['data.json', 'logo.txt', 'users.json', 'pics/*.png'],
}
entry_points = {
    'console_scripts': [
        'snake=snake.main:main',
    ],
}
setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=author,
    author_email=author_email,
    url=url,
    package_data=package_data,
    include_package_data=True,
    packages=find_packages(),
    install_requires=install_requires,
    entry_points=entry_points,
)
