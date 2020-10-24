# file to hanle network file (model/net.pth)
import os 
import requests

# class to handle model file
class NetManager:
    def __init__(self, url='https://hosting.greerpage.com/files/greer_page/net.pth'):
        self.path = os.path.abspath('model/net.pth')
        self.installed = os.path.isfile(self.path)
        self.url = url

    def install(self):
        '''download and install the pre-trained net.pth file'''
        if self.installed:
            print('model already installed')
            return
        r = requests.get(self.url, allow_redirects=True)
        print('downloading model...')
        os.mkdir('model')
        open('model/net.pth', 'wb').write(r.content)
        return self.path

