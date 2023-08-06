def test_installation():
    '''
    Test the installation
    '''
    
    import pkg_resources
    PYNUFFT_PATH = pkg_resources.resource_filename('pynufft', './')
    DATA_PATH = pkg_resources.resource_filename('pynufft', 'data/')
    import os.path
    
    
    print('Does pynufft.py exist? ',os.path.isfile(PYNUFFT_PATH+'pynufft.py'))
    print('Does om1D.npz exist?',os.path.isfile(DATA_PATH+'om1D.npz'))
    print('Does om2D.npz exist?',os.path.isfile(DATA_PATH+'om2D.npz'))
    print('Does om3D.npz exist?',os.path.isfile(DATA_PATH+'om3D.npz'))
    print('Does phantom_3D_128_128_128.npz exist?', os.path.isfile(DATA_PATH+'phantom_3D_128_128_128.npz'))
    print('Does phantom_256_256.npz exist?', os.path.isfile(DATA_PATH+'phantom_256_256.npz'))
    print('Does 1D_example.py exist?', os.path.isfile(PYNUFFT_PATH+'example/1D_example.py'))
    print('Does 2D_example.py exist?', os.path.isfile(PYNUFFT_PATH+'example/1D_example.py'))


if __name__ == '__main__':
    test_installation()