from setuptools import setup

setup(name='CTRegisterMicroserviceFlask',
      version='0.1.2',
      description='Library for interact in the microservice with the Control-tower api-gateway (register,  do request to other microservices, etc)',
      author='Sergio Gordillo',
      author_email='sergio.gordillo@vizzuality.com',
      license='MIT',
      packages=['CTRegisterMicroserviceFlask'],
      tall_requires=[
        'flask',
        'requests'
      ],
      zip_safe=False)
