import streamlit as st


def leven_dist_func(source, target):
    d_matrix = [[0]*(len(target)+1) for _ in range(len(source)+1)]

    for j in range(len(target) + 1):
        d_matrix[0][j] = j

    for i in range(1, len(source) + 1):
        d_matrix[i][0] = i

    for row in range(1, len(source) + 1):
        for col in range(1, len(target) + 1):
            if (source[row-1] == target[col-1]):
                d_matrix[row][col] = d_matrix[row - 1][col - 1]
            else:
                d_del = d_matrix[row - 1][col] + 1
                d_ins = d_matrix[row][col - 1] + 1
                d_sub = d_matrix[row - 1][col - 1] + 1
                d_matrix[row][col] = min(d_del, d_ins, d_sub)

    return d_matrix[len(source)][len(target)]


def preprocess_vocab(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    words = sorted(set([line.strip().lower() for line in lines]))
    return words


def slit_leven_func():
    vocabs = preprocess_vocab("data/vocab.txt")
    st.title("Word Correction using Levenshtein Distance")
    source = st.text_input("Word:")

    if st.button("Compute"):
        leven_dist = dict()
        for vocab in vocabs:
            leven_dist[vocab] = leven_dist_func(source, vocab)

        sorted_dist = dict(
            sorted(leven_dist.items(), key=lambda item: item[1]))
        correct_word = list(sorted_dist.keys())[0]
        st.write('Correct word: ', correct_word)
        st.markdown(
            '<div style="text-align: center;">Other words</div>', unsafe_allow_html=True)
        st.divider()

        col1, col2 = st.columns(2)
        for key, value in list(sorted_dist.items())[1:3]:
            col1.write(f"{key}: {value}")

        for key, value in list(sorted_dist.items())[3:5]:
            col2.write(f"{key}: {value}")


if __name__ == "__main__":
    slit_leven_func()
