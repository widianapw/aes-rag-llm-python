def normalize_score(rubrics, score):
    try:
        #rubrics = "\nScore 1: asdsad.\n Score 2: adasdasasd asdad.\nScore 3: asdasd asdasd asdasd.\nScore 4: asdasd asdasd asdasd asdasd.\nScore 5: asdasd asdasd asdasd asdasd asdasd.
        available_scores = [int(s.split(":")[0].split(" ")[-1]) for s in rubrics.split("\n") if s]
        print("Avaliable Scores: ", available_scores)
        if score in available_scores:
            return score
        else:
            print("Out of range: "+score)
            if score > 5:
                return 5
            elif score < 1:
                return 1
            else:
                for i in range(len(available_scores)):
                    if score > available_scores[i]:
                        return available_scores[i]
                    elif score < available_scores[i]:
                        return available_scores[i]
                    else:
                        return score
    except Exception as e:
        print(e)
        return score