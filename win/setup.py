"""
Setup script for Cash Register Connection Monitor
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Cash Register Connection Monitor - A Windows system tray application for monitoring cash register connectivity"

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="datecs-cash-register-monitor",
    version="1.0.0",
    author="Dimitar Klaturov",
    description="A Windows system tray application for monitoring Datecs cash register connectivity",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/dimitarklaturov/datecs-cash-register-monitor",
    packages=find_packages(),
    package_data={
        'cash_register_monitor': ['icons/*.ico', 'icons/*.png'],
    },
    include_package_data=True,
    install_requires=read_requirements(),
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'black>=21.0',
            'flake8>=3.8',
        ],
        'build': [
            'pyinstaller>=4.5',
            'auto-py-to-exe>=2.0',
        ]
    },
    entry_points={
        'console_scripts': [
            'datecs-cash-register-monitor=cash_register_monitor.main:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Networking :: Monitoring",
        "Environment :: Win32 (MS Windows)",
    ],
    python_requires=">=3.8",
    keywords="datecs, cash register, monitoring, network, connectivity, windows, system tray",
    project_urls={
        "Bug Reports": "https://github.com/dimitarklaturov/datecs-cash-register-monitor/issues",
        "Source": "https://github.com/dimitarklaturov/datecs-cash-register-monitor",
        "Documentation": "https://github.com/dimitarklaturov/datecs-cash-register-monitor/wiki",
    },
)