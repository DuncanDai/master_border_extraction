import cv2
import numpy as np

# absolute path
PATH_IMAGE = 'D:\\My_Data\\me_Docs\\Masterarbeit\\master_border_extraction\\images\\test1.png'

def homomorphic_filter(src, d0=10, gamma_h=2.5, gamma_l=0.5, c=1):
    # grayscale image
    gray = src.copy()   
    # if src is not grayscale
    if len(src.shape) > 2:
        gray = cv2.cvtcolor(src, cv2.COLOR_BGR2GRAY)
    
    # image format
    gray = np.float32(gray)   # or np.float64(gray)
    # logarithm
    gray = np.log(gray + 1.0)
    # normalization
    gray = gray / np.log(256)  

    # FFT
    gray_fft = np.fft.fft2(gray)
    gray_fftshift = np.fft.fftshift(gray_fft)

    # create arithmetic arrays
    rows, cols = gray.shape
    M, N = np.meshgrid(np.arange(-cols // 2, cols // 2),
                        np.arange(-rows // 2, rows // 2))

    # filtering in frequency domain
    D = np.sqrt(M ** 2 + N ** 2)   # D is the distance from the center
    H = (gamma_h - gamma_l) * (1 - np.exp(-c * (D ** 2 / d0 ** 2))) + gamma_l  # high pass filter
    dst_fftshift = H * gray_fftshift

    # inverse FFT
    dst_ifftshift = np.fft.ifftshift(dst_fftshift)
    dst_ifft = np.fft.ifft2(dst_ifftshift)

    # get the modulus of imaginary numbers
    dst = np.abs(dst_ifft)

    # inverse logarithm
    dst = np.exp(dst) - 1
    dst = (dst - dst.min()) / (dst.max() - dst.min()) # standardization
    dst *= 255

    # image format
    dst = np.uint8(np.clip(dst, 0, 255))
    return dst

if __name__ == "__main__":
    img = cv2.imread(PATH_IMAGE, cv2.IMREAD_GRAYSCALE)  # img = cv2.resize(img, (400, 400))
    img_homo_filtered = homomorphic_filter(img)

    contrast = np.hstack((img, img_homo_filtered))

    cv2.namedWindow("contrast", cv2.WINDOW_NORMAL) 
    cv2.imshow('contrast', contrast)
    cv2.waitKey()
    cv2.destroyAllWindows()