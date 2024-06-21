import pydicom
import cv2
import numpy as np
import os

def load_dicom_images_from_directory(directory):
    frames = []
    
    for filename in sorted(os.listdir(directory)):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and filepath.lower().endswith('.dcm'):
            try:
                # Carregar o arquivo DICOM
                dataset = pydicom.dcmread(filepath)
                frames.append(dataset.pixel_array)
                print(f"Carregado: {filepath}")
            except Exception as e:
                print(f"Erro ao carregar {filepath}: {e}")
    
    return frames

def adjust_brightness(frames, scale_factor):
    adjusted_frames = []
    for frame in frames:
        # Multiplicar os valores dos pixels pelo fator de escala
        adjusted_frame = frame * scale_factor
        # faixa válida de 0-255
        adjusted_frame = np.clip(adjusted_frame, 0, 255).astype(np.uint8)
        adjusted_frames.append(adjusted_frame)
    return adjusted_frames

def save_video(frames, output_file, frame_rate):
    if not frames:
        print("Nenhum frame para salvar.")
        return

    # Determinar a dimensão das imagens
    height, width = frames[0].shape
    
    # Criar o vídeo
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter(output_file, fourcc, frame_rate, (width, height), isColor=False)
    
    for frame in frames:
        try:
            # Converter o frame para 8 bits se necessário
            if frame.dtype != np.uint8:
                frame = (255 * (frame - np.min(frame)) / (np.max(frame) - np.min(frame))).astype(np.uint8)
            
            # Adicionar o frame ao vídeo
            video.write(frame)
        except Exception as e:
            print(f"Erro ao processar frame: {e}")
    
    # Liberar o vídeo
    video.release()
    print(f"Vídeo salvo como {output_file}")

# Caminho para o diretório contendo os arquivos DICOM
dicom_directory = r'Diretório das imagens DICOM'
# Caminho para o arquivo de saída do vídeo
output_file = r'Diretório para por o arquivo .avi'
# Taxa de quadros do vídeo
frame_rate = 10
# Fator de escala para ajustar o brilho
brightness_scale_factor = 0.1  #(1.5 aumenta o brilho em 50%)

# Carregar as imagens do diretório de arquivos DICOM
frames = load_dicom_images_from_directory(dicom_directory)

# Verifique se carregou algum frame
if not frames:
    print("Nenhum arquivo DICOM encontrado no diretório especificado.")
else:
    # Ajustar o brilho das imagens
    frames = adjust_brightness(frames, brightness_scale_factor)
    
    # Salvar as imagens como um vídeo
    save_video(frames, output_file, frame_rate)

# Verificar se o arquivo de vídeo foi criado com sucesso
if os.path.isfile(output_file):
    print("O arquivo de vídeo foi criado com sucesso.")
else:
    print("O arquivo de vídeo não foi criado.")
