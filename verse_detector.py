from pychorus import create_chroma
from pychorus import find_and_output_chorus
from pychorus.similarity_matrix import TimeTimeSimilarityMatrix, TimeLagSimilarityMatrix

def show_details(path):
    chroma, _, sr, _ = create_chroma(path)
    time_time_similarity = TimeTimeSimilarityMatrix(chroma, sr)
    time_lag_similarity = TimeLagSimilarityMatrix(chroma, sr)


    # Visualize the results
    time_time_similarity.display()
    time_lag_similarity.display()

    #https://github.com/vivjay30/pychorus

def find_chorus(path):
    return find_and_output_chorus(path, "beat_file/chorus.wav", 10)