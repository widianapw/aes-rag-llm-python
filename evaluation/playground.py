from sklearn.metrics import cohen_kappa_score

a = [1,3,5]
b = [1,1,5]
print(a)
print(b)
print("QWK",cohen_kappa_score(a, b, weights="quadratic"))