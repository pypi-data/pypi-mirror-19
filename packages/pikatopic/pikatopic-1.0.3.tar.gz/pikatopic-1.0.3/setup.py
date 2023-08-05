from setuptools import setup

setup(name='pikatopic',
      version='1.0.3',
      description='A convenience layer atop Pika for use with RabbitMQ topic exchanges.',
      url='http://github.com/AnimationMentor/pikatopic',
      author='Reed Wade for Artella.com',
      author_email='reed@artella.com',
      license='MIT',
      packages=['pikatopic'],
      install_requires=[
          'pika',
      ],
      )
