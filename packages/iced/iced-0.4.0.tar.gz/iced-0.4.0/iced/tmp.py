def _filter_low_coverage(X, mincov=5, verbose=False):
    """
    Filter rows and columns with low counts

    Parameters
    ----------
    X : ndarray (n, n)
        Count matrix (hollow, symetric)

    mincov : integer, default: 5
        rows and columns with less counts are discarded

    Return
    ------
    X : ndarray (n, n)
        The filtered array
    """
    X_sum = np.array(X.sum(axis=0)).flatten()

    if verbose:
        print("Filter %s bins ..." % sum(X_sum < mincov))

    if sparse.issparse(X):
        _filter_csr(X, (X_sum < mincov))
    else:
        X[X_sum < mincov, :] = np.nan
        X[:, X_sum < mincov] = np.nan

    return X



