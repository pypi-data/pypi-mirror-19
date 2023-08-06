from setuptools import setup
def main():
     setup(
          name='belalscript',    # This is the name of your PyPI-package.
          version='0.3',                          # Update the version number for new releases
          entry_points={
                      'console_scripts': [
                          'belalscript = belalscript.application:main',  # noqa: E501
                      ]},
          scripts=['belalscript']                  # The name of your scipt, and also the command you'll be using for calling it
     )
if __name__ == '__main__':
    main()