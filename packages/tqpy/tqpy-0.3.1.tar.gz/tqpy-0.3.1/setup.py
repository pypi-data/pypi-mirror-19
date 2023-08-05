from setuptools import setup, find_packages


setup(name="tqpy",
      version="0.3.1",
      description="""A compact, scalable, statistical analysis, and reporting package built on top of
                     pandas, used to assist in Yahoo! Traffic Quality investigations.""",
      author="Rashad Alston",
      author_email="ralston@yahoo-inc.com",
      url="https://www.github.com/notslar-ralston/tqpy",
      packages=find_packages(),
      package_data={"": ["LICESNSE.txt", "README.md", "requirements.txt"]},
      include_package_data=True,
      platforms="any",
      license="BDS 3 Clause",
      install_requires=["numpy", "matplotlib", "pandas", "bokeh"],
      zip_safe=False,
      long_description="""

            A compact, scalable, statistical analysis and reporting package built on top of
            pandas, used to assist in Yahoo! Traffic Quality investigations.

            Contact
            -------
            If you have any questions or comments about dataRX, please feel free to contact me via
            email at ralston@yahoo-inc.com.
            This project is hosted at: https://www.github.com/notslar-ralston
            The documentation can be found at: https://www.github.com/notslar-ralston/tqpy
      """)
