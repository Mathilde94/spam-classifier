def precision(tp, fp, fn, tn):
    return float(tp) / float(tp + fp)


def recall(tp, fp, fn, tn):
    return float(tp) / float(tp + fn)


def f1_score(tp, fp, fn, tn):
    p = precision(tp, fp, fn, tn)
    r = recall(tp, fp, fn, tn)

    return float(2 * p * r) / float(p + r)


def show_results(tp, fp, fn, tn, S, NS):
    print("*" * 50)
    print("Correctness for spam: ", tp, fn, S)
    print("Correctness for no-spam: ", tn, fp, NS)
    print(tp, tn, fp, fn)
    print("Precision: ", precision(tp, fp, fn, tn))
    print("Recall", recall(tp, fp, fn, tn))
    print("F1 score", f1_score(tp, fp, fn, tn))
