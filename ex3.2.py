import scipy.stats as ss
import numpy as np
import matplotlib.pyplot as plt


def main():
    # Example 3.3:  Comparing Normal Means: Independent Sampling ###
    n1 = 24
    ybar1 = 7.8730
    s1 = 0.05353
    n2 = 123
    ybar2 = 7.9725
    s2 = 0.01409
    # Independent draws from posterior ...
    Nsim = 100000
    sigma1_2s = 1 / ss.gamma.rvs(a=(n1 - 1) / 2, scale=1 / (((n1 - 1) * s1 ** 2) / 2), size=Nsim)
    sigma2_2s = 1 / ss.gamma.rvs((n2 - 1) / 2, 1 / (((n2 - 1) * s2 ** 2) / 2), size=Nsim)
    mu1s = ss.norm.rvs(ybar1, np.sqrt(sigma1_2s / n1), size=Nsim)
    mu2s = ss.norm.rvs(ybar2, np.sqrt(sigma2_2s / n2), size=Nsim)
    # Posterior inference based on empirical distribution of draws ...
    # approx. posterior density curve for mu1 - mu2 (histogram and smooth)
    x_train = mu1s - mu2s
    x_test = np.linspace(-0.15, -0.05, 1000)
    density = ss.gaussian_kde(x_train)
    y = density(x_test)

    fig, ax1 = plt.subplots()
    ax1.hist(x_train, bins=16, color="grey", ec="k", density=True)
    ax1.plot(x_test, y, c='b')
    plt.show()
    print(1)
    pass


if __name__ == "__main__":
    main()
