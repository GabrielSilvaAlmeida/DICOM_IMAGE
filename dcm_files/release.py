import cv2

# Caminho para o arquivo de vídeo
video_file = r'E:\My project\dcm_files\output2_video.avi'

# Capturar o vídeo do arquivo
cap = cv2.VideoCapture(video_file)

if not cap.isOpened():
    print("Erro ao abrir o arquivo de vídeo.")
else:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Exibir o frame
        cv2.imshow('Video', frame)
        
        # Pressione 'q' para sair do loop de visualização
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Liberar o objeto de captura e fechar todas as janelas
    cap.release()
    cv2.destroyAllWindows()